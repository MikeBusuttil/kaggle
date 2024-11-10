from os import environ
from pymongo import MongoClient
from sklearn.metrics import root_mean_squared_error
from numpy import log1p
from sigfig import round

from bson.codec_options import CodecOptions
from zoneinfo import ZoneInfo
EDT = ZoneInfo('America/Toronto')

credentials = {
    'host': 'db',
    'username': 'root',
    'password': environ.get('DB_KEY')
}
options = {'codec_options': CodecOptions(tz_aware=True, tzinfo=EDT)}

def initialize():
    # handle case where collection already exists
    dump = MongoClient(**credentials).dump
    dump.create_collection("measurements")

def store(payload):
    if not payload:
        return None
    client = MongoClient(**credentials)
    client.dump.measurements.insert_many(payload)

def rmse(filter):
    search_criteria = filter
    output_format = {
        '_id':0, 
        'SalePrice':1, 
        'predictions': 1,
    }
    readings = MongoClient(**credentials).dump.measurements.with_options(**options)
    results = readings.find(search_criteria, output_format)
    predicted, actual = [], []
    for r in results:
        predicted.append(r["predictions"])
        actual.append(r["SalePrice"])
    output = root_mean_squared_error(log1p(predicted), log1p(actual))
    return output

def get(filter):
    search_criteria = filter
    readings = MongoClient(**credentials).dump.measurements.with_options(**options)
    results = readings.find(search_criteria)
    return list(results)

def combinations(fields):
    readings = MongoClient(**credentials).dump.measurements.with_options(**options)
    results = readings.aggregate([
        {
            "$group": {
                "_id": { field: f"${field}" for field in fields },
                "totalRecords": { "$count": {} },
                # "totalIterations": { "$sum": 1/1450 },
            },
        }
    ])
    return results

def score_combinations():
    output = []
    fields = [
        "n_estimators",
        "learning_rate",
        "max_depth",
        'max_features',
        'min_samples_leaf',
        'min_samples_split',
        'loss',
        'random_state',
    ]
    for f in combinations(fields):
        output.append(f["_id"] | {
            "score": rmse({field: f["_id"][field] for field in fields}),
            "totalRecords": f["totalRecords"],
            "totalIterations": f["totalRecords"]/1450
        })
    return output

if __name__ == '__main__':
    # filter = {
    #     "n_estimators": 500,
    #     "learning_rate": .1,
    #     "max_depth": 1,
    #     'max_features': 'sqrt',
    #     'min_samples_leaf': 15,
    #     'min_samples_split': 10, 
    #     'loss': 'huber',
    #     'random_state': 42,
    # }
    #print(score_combinations())
    initialize()
