import json
import requests
import openai
import keys
from datetime import datetime


# MET OFFICE
MET_OFFICE_API_KEY = keys.MET_OFFICE_API_KEY

# Five day forecast
FORECAST_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"
FORECAST_LOCATION = keys.FORECAST_LOCATION
FORECAST_RESOLUTION = "3hourly"
FORECAST_5DAYS = FORECAST_URL + FORECAST_LOCATION + \
    "?res=" + FORECAST_RESOLUTION + "&key=" + MET_OFFICE_API_KEY

# Observed weather
OBSERVED_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/"
OBSERVED_LOCATION = keys.OBSERVED_LOCATION
OBSERVED_RESOLUTION = "hourly"
OBSERVED_24HOURS = OBSERVED_URL + OBSERVED_LOCATION + \
    "?res=" + OBSERVED_RESOLUTION + "&key=" + MET_OFFICE_API_KEY

# Historical weather
HISTORICAL_URL = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/"
HISTORICAL_LOCATION = keys.HISTORICAL_LOCATION
HISTORICAL_DATA = HISTORICAL_URL + HISTORICAL_LOCATION + ".txt"

# OPENAI
OPENAI_KEY = keys.OPENAI_API_KEY


class Forecast(object):
    def __init__(self, FORECAST_5DAYS):
        self.FORECAST_5DAYS = FORECAST_5DAYS

    def update(self):
        forecast = requests.get(FORECAST_5DAYS).text
        forecast = json.loads(forecast)

        with open("debug_future.json", "w") as write_file:
            json.dump(forecast, write_file, indent=4)

        # today = data["SiteRep"]["DV"]["FORECAST_Location"]["Period"][0]["Rep"]
        # today.pop(0)

    def get_parameters(self):
        file_path = 'debug_future.json'

        with open(file_path, 'r') as f:
            data = json.load(f)

        params = data["SiteRep"]["Wx"]["Param"]
        param_dict = {}

        for param in params:
            name = param["name"]
            param_dict[name] = {
                "unit": param["units"],
                "description": param["$"]
            }

        return param_dict

    def parse_period_data(self):

        file_path = 'debug_future.json'
        with open(file_path, 'r') as f:
            data = json.load(f)

        periods = data["SiteRep"]["DV"]["Location"]["Period"]
        period_data = {}

        for period in periods:
            period_value = period["value"]
            period_data[period_value] = {}

            for rep in period["Rep"]:
                rep_key = rep["$"]
                rep_data = {key: value for key,
                            value in rep.items() if key != "$"}
                period_data[period_value][rep_key] = rep_data

        return period_data

    def create_string_list(self, parsed_data, parsed_period_data):

        result_list = []

        for period_key, period_data in parsed_period_data.items():
            dt = datetime.strptime(period_key, '%Y-%m-%dZ')
            day_of_week = dt.strftime('%A')
            for time_key, time_data in period_data.items():
                time_str = convert_to_hour(int(time_key))
                result_str = f"{day_of_week} @ {time_str}."
                for param_key, param_value in time_data.items():
                    if param_key in parsed_data:
                        param_desc = parsed_data[param_key]["description"]
                        param_units = parsed_data[param_key]["unit"]
                        param_str = f" {param_desc}: {param_value}{param_units},"
                        result_str += param_str
                # Remove the trailing comma and add the result string to the list
                result_list.append(result_str[:-1])

        return result_list

# Function to convert time to hour in 00:00 format


def convert_to_hour(time):
    hours, minutes = divmod(time, 60)
    return f"{hours:02d}:{minutes:02d}"


if __name__ == "__main__":
    forecast = Forecast(FORECAST_5DAYS)
    # forecast.update()

    # Replace 'path/to/your/json_file.json' with the path to the JSON file you want to read
    parsed_data = forecast.get_parameters()
    print(parsed_data)
    parsed_period_data = forecast.parse_period_data()
    print(parsed_period_data)
    result_list = forecast.create_string_list(parsed_data, parsed_period_data)
    print(result_list)
