import json
import requests
import openai
import keys
from datetime import datetime, timedelta


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
    def __init__(self):
        self.FORECAST_5DAYS = FORECAST_5DAYS
        self.OBSERVED_24HOURS = OBSERVED_24HOURS

    def update(self):
        # Get forecast data from Met Office API
        forecast = requests.get(FORECAST_5DAYS).text
        forecast = json.loads(forecast)

        # Save forecast data to debug file
        with open("debug_forecast.json", "w") as write_file:
            json.dump(forecast, write_file, indent=4)

        return forecast

    def parse_period_data(self):

        file_path = 'debug_forecast.json'
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

    def create_string_list(self, parsed_period_data):

        result_list = []

        # Get params from params.json
        with open("params.json", "r") as f:
            params = json.load(f)

        # Convert the parsed data into a list of strings
        for period_key, period_data in parsed_period_data.items():
            day_of_week = convert_to_day(period_key)
            for time_key, time_data in period_data.items():
                time_str = convert_to_hour(int(time_key))
                result_str = f"{day_of_week.upper()} @ {time_str}."
                for param_key, param_value in time_data.items():
                    if param_key in params:
                        param_desc = params[param_key]["description"]
                        param_units = params[param_key]["unit"]

                        try:
                            param_value = str(round(float(param_value)))
                        except ValueError:
                            pass

                        try:
                            param_def = params[param_key]["definition"]
                            param_value = param_def[param_value]
                        except KeyError:
                            pass

                        param_str = f" {param_desc}: {param_value}{param_units},"
                        result_str += param_str
                # Remove the trailing comma and add the result string to the list
                result_list.append(result_str[:-1])

        return result_list


def convert_to_day(date):
    # Function to convert date to day of the week

    # Check if the input date is today or tomorrow or yesterday
    date = datetime.strptime(date, "%Y-%m-%dZ")
    today = datetime.now().date()
    if date.date() == today:
        return "Today"
    elif date.date() == today + timedelta(days=1):
        return "Tomorrow"
    elif date.date() == today - timedelta(days=1):
        return "Yesterday"

    # Get the day of the week
    day_of_week = date.strftime("%A")
    return day_of_week


def convert_to_hour(time):
    # Function to convert time to hour in 00:00 format

    hours, minutes = divmod(time, 60)
    return f"{hours:02d}:{minutes:02d}"


if __name__ == "__main__":
    forecast = Forecast()
    forecast.update()

    # Replace 'path/to/your/json_file.json' with the path to the JSON file you want to read
    parsed_period_data = forecast.parse_period_data()
    result_list = forecast.create_string_list(parsed_period_data)
    print(result_list)
