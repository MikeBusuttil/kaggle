from json import loads
from os import path

raw = loads(open(f"{path.dirname(__file__)}/inflation.json").read())["observations"]

inflation_data = {}
for obs in raw:
    inflation_data[obs["d"][:7]] = float(obs["STATIC_INFLATIONCALC"]["v"])

def adjust(price=0, year=0, month=7, base_year=2010, base_month=7):
    if not year or not price:
        raise ValueError("Year and price must be provided")
    return price * inflation_data[f"{base_year}-{base_month:02}"] / inflation_data[f"{year}-{month:02}"]
