from json import loads
from os import path

raw = loads(open(f"{path.dirname(__file__)}/inflation.json").read())["observations"]

inflation_data = {}
for obs in raw:
    inflation_data[obs["d"][:7]] = float(obs["STATIC_INFLATIONCALC"]["v"])

def adjust(price=0, from_year=0, from_month=7, to_year=2010, to_month=7):
    input_type = type(price)
    if not from_year or not price:
        raise ValueError("Year and price must be provided")
    return input_type(price * inflation_data[f"{to_year}-{to_month:02}"] / inflation_data[f"{from_year}-{from_month:02}"])
