from numpy import exp, std
from sigfig import round
import pandas as pd
from random import shuffle
from datetime import datetime, timedelta
from itertools import product
from requests import post
from os import environ
from pathlib import Path

max_iterations = 50
max_duration = timedelta(minutes=15)
max_streak = 20
streak = {
    "value": None,
    "count": 0,
}
hpo_grid_options = {
    "n_estimators": [500, 1_000, 3_000],
    "learning_rate": [.1, .05, .01],
    "max_depth": [n for n in range(1, 7)],
    'max_features': ['sqrt'],
    'min_samples_leaf': [15],
    'min_samples_split': [10], 
    'loss': ['huber'],
    'random_state': [42, 420],
}

authorization = {"key": environ.get("AGENT_KEY")}
url = "https://dump.techiteasy.ca"
data = pd.read_csv(Path(__file__).parent / 'mike_all.csv')
full_training_data = data.drop(data[data["SalePrice"].isna()].index)
original_data = pd.read_csv(Path(__file__).parent / 'train.csv')
scores = []

def time_stamp(date=None):
    if not date:
        date = datetime.now()
    return date.strftime('%-d-%b-%y %-I:%M:%S.%f')[:-3] + date.strftime(' %p').lower()
def log(*args):
    print(f'[{time_stamp()}]', *args)

def store_predictions(predictions, params, model=""):
    for param, value in params.items():
        predictions[param] = value
    predictions["model"] = model
    post(f"{url}/store", json={"records": predictions.to_dict('records')} | authorization)

def stopped_changing(score):
    global scores, streak
    scores.append(score)
    score = round(score, std(scores), format='Drake')
    if score == streak["value"]:
        streak["count"] += 1
    else:
        streak["count"] = 0
        streak["value"] = score
    if streak["count"] > max_streak:
        return True
    return False

def its_time_to_stop(params={}, elapsed=None, iterations=None, model=""):
    if elapsed > max_duration:
        return True
    if iterations > max_iterations:
        return True
    score = post(f"{url}/rmse", json={"filter": params|{"model": model}} | authorization).json()
    if stopped_changing(score):
        return True
    return False

def generate_cross_validation_sets(data=data, sets=5):
    ids = data["Id"].to_list()
    shuffle(ids)
    set_size = len(data) // sets
    for n in range(sets):
        yield sorted(ids[n*set_size:(n+1)*set_size])

def split(data=None, test_ids=None):
    training_data = data.drop(data[data["Id"].isin(test_ids)].index)
    training_data = training_data[training_data["SalePrice"].notna()]
    training_price = training_data["SalePrice"]
    validation_data = data[data["Id"].isin(test_ids)]
    validation_price = validation_data["SalePrice"]
    return training_data, training_price, validation_data.copy(), validation_price

from sklearn.ensemble import GradientBoostingRegressor
def cross_validate(test_ids, params={}):
    training_data, training_price, validation_data, validation_price = split(data=full_training_data, test_ids=test_ids)

    missing_columns = (set(validation_data.columns) - set(training_data.columns) | set(training_data.columns) - set(validation_data.columns)) - set(["SalePrice", "Id"])
    if missing_columns:
        log("the following columns exist in only 1 data set", list(missing_columns))
    training_data.drop(list(missing_columns), axis=1, inplace=True, errors='ignore')
    validation_data.drop(list(missing_columns), axis=1, inplace=True, errors='ignore')

    model = None
    model = GradientBoostingRegressor(**params)
    model.fit(training_data.drop(["SalePrice", "Id"], axis=1), training_price)

    predictions = model.predict(validation_data.drop(["SalePrice", "Id"], axis=1))
    predictions = exp(predictions)

    validation_price_original = original_data[original_data["Id"].isin(validation_data["Id"].to_list())]["SalePrice"]

    details = pd.DataFrame({"SalePrice": validation_price_original, "predictions": predictions})
    details["Id"] = details.index
        
    return details

def generate_cross_validation_sets(data=full_training_data, sets=10):
    ids = data["Id"].to_list()
    shuffle(ids)
    set_size = len(data) // sets
    for n in range(sets):
        yield sorted(ids[n*set_size:(n+1)*set_size])

def hpo_grid(grid_options):
    keys = list(grid_options.keys())
    values = list(grid_options.values())
    for combination in product(*values):
        yield dict(zip(keys, combination))

options = len([_ for _ in hpo_grid(hpo_grid_options)])
for option, params in enumerate(hpo_grid(hpo_grid_options)):
    scores = []
    start_time = datetime.now()
    iterations = 0
    log(f"{option}/{options}: finding exact score for params", params)
    while True:
        iterations += 1
        validation_id_sets = generate_cross_validation_sets(data=full_training_data, sets=10)
        for validation_ids in validation_id_sets:
            predictions = cross_validate(validation_ids, params=params)
            store_predictions(predictions, params, model="gbr")
        log(f"{iterations}. score of {streak['value']} unchanged in {streak['count']} iterations")
        if its_time_to_stop(params=params, elapsed=datetime.now()-start_time, iterations=iterations, model="gbr"):
            break
    log(f"stopped after {datetime.now() - start_time} elapsed")
