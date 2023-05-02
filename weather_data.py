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


class OpenAI(object):

    def get(self, prompt):
        openai.api_key = OPENAI_KEY

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=128,
            top_p=1,
            frequency_penalty=2,
            presence_penalty=2
        )

        return response


class Weather(object):
    def __init__(self):
        pass

    def update(self, source_url):

        # Get forecast data from Met Office API
        data = requests.get(source_url).text
        data = json.loads(data)

        # Save forecast data to debug file
        with open("debug_forecast.json", "w") as write_file:
            json.dump(data, write_file, indent=4)

        # Parse the data into a dictionary
        periods = data["SiteRep"]["DV"]["Location"]["Period"]
        d = {}

        for period in periods:
            report_date = period["value"]
            for report in period["Rep"]:
                time = report["$"]
                report_datetime = self._convert_to_datetime(report_date, time)
                report_data = {key: value for key,
                               value in report.items() if key != "$"}
                d[report_datetime] = report_data

        return d

    def weather_to_strings(self, data):

        result_list = []

        # Get params from params.json
        with open("params.json", "r") as f:
            params = json.load(f)

        # Convert the parsed data into a list of strings
        for report_datetime, report_data in data.items():

            # Convert datetime to date and HH:MM string
            day_of_week = self._convert_to_day_string(report_datetime)
            time_str = report_datetime.strftime('%l %p')
            result_str = f"{day_of_week} @ {time_str}:"

            # Add the report data to the result string
            for param_key in params.keys():
                if param_key in report_data.keys():
                    param_value = report_data[param_key]
                    # param_desc = params[param_key]["description"]
                    param_ignore = params[param_key]["ignore"]
                    param_units = params[param_key]["unit"]
                    if param_ignore == False:
                        try:
                            param_value = str(round(float(param_value)))
                        except ValueError:
                            pass
                        try:
                            param_def = params[param_key]["definition"]
                            param_value = param_def[param_value]
                        except KeyError:
                            pass

                        param_str = f" {param_value}{param_units},"
                        result_str += param_str
                # Remove the trailing comma and add the result string to the list
            result_list.append(result_str[:-1])

        return result_list

    def _convert_to_day_string(self, date):
        # Check if the input date is today or tomorrow or yesterday
        today = datetime.now().date()
        if date.date() == today:
            return "Today"
        elif date.date() == today + timedelta(days=1):
            return "Tomorrow"
        elif date.date() == today - timedelta(days=1):
            return "Yesterday"

        # Return the day of the week
        return date.strftime("%A")

    def _convert_to_datetime(self, date, time):
        # Function to convert date and time strings to datetime object
        date = datetime.strptime(date, "%Y-%m-%dZ")
        # Convert time to datetime.time by first dividing by 60
        hours = int(time) // 60
        minutes = int(time) % 60
        time = datetime.strptime(f"{hours}:{minutes}", "%H:%M").time()

        # Combine date and time into a datetime object

        return datetime.combine(date, time)


if __name__ == "__main__":

    # Get the weather forecast from the Met Office API
    weather = Weather()
    timenow = datetime.now()
    # timenow = timenow.replace(hour=11)

    # Get the observed weather from the Met Office API
    observed = weather.update(OBSERVED_24HOURS)

    # Convert data to 3h intervals
    observed = {key: value for key,
                value in observed.items() if key.hour % 3 == 0}

    # If time is before midday, discard data from today and from after 9pm yesterday
    if timenow.hour < 12:
        observed = {key: value for key, value in observed.items() if key <
                    timenow.replace(hour=21, minute=0, second=0) - timedelta(days=1)}

    # If time is after midday, discard data from yesterday and before 6am today
    elif timenow.hour >= 12:
        observed = {key: value for key, value in observed.items() if key >
                    timenow.replace(hour=5, minute=59, second=59)}

    # Convert the observed data to a list of strings
    observed = weather.weather_to_strings(observed)

    print("Past:")
    for item in observed:
        print(item)

    # Get the forecast weather from the Met Office API
    forecast = weather.update(FORECAST_5DAYS)

    # Discard forecast data older than 3 hours ago
    forecast = {key: value for key, value in forecast.items() if key >
                timenow - timedelta(hours=3)}

    # Discard data past the end of today
    forecast = {key: value for key, value in forecast.items() if key <
                timenow.replace(hour=23, minute=59, second=59)}

    # Convert the forecast data to a list of strings
    forecast = weather.weather_to_strings(forecast)

    print("Future forecast:")

    for item in forecast:
        print(item)

    print("Give a two-sentence, qualitative summary/comparison of the forecast:")
