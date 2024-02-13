#!/usr/bin/env python3
import json
import requests
from openai import OpenAI
from datetime import datetime, timedelta
from random import choice
import csv
import os

import dotenv

dotenv.load_dotenv()

MET_OFFICE_API_KEY = os.getenv("MET_OFFICE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FORECAST_LOCATION = os.getenv("FORECAST_LOCATION")
OBSERVED_LOCATION = os.getenv("OBSERVED_LOCATION")
HISTORICAL_LOCATION = os.getenv("HISTORICAL_LOCATION")

FORECAST_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"
FORECAST_RESOLUTION = "3hourly"
FORECAST_5DAYS = f"{FORECAST_URL}{FORECAST_LOCATION}?res={FORECAST_RESOLUTION}&key={MET_OFFICE_API_KEY}"

OBSERVED_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/"
OBSERVED_RESOLUTION = "hourly"
OBSERVED_24HOURS = f"{OBSERVED_URL}{OBSERVED_LOCATION}?res={OBSERVED_RESOLUTION}&key={MET_OFFICE_API_KEY}"

HISTORICAL_URL = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/"
HISTORICAL_DATA = f"{HISTORICAL_URL}{HISTORICAL_LOCATION}.txt"


class LLM:
    def __init__(self):
        pass

    def call_api(self, prompt):
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                "role": "system",
                "content": f"{prompt['system']}"
                },
                {
                "role": "user",
                "content": f"{prompt['user']}"
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content 

    def summarise_forecast(self, forecast):
        system = "You are an intelligent assistant that summarises the weather forecast. Answer as concisely as possible."
        user = forecast + "\n" + "Summarise the above forecast. Include useful information such as whether it will rain, the strength of wind and temperature. Comparing today's weather to yesterday's weather is particularly useful, if that information is avaliable."

        prompt = {
            "system": system,
            "user": user
        }

        response = self.call_api(prompt)

        return response


    def change_style(self, forecast, style):
        system = "You are a funny assistant that changes the style of weather reports. You are not a weather reporter, so you don't need to be specific about the metrics, just descriptive and you can use more casual language. Answer as concisely as possible."
        user = "Change the following to the style of " + \
            style + ": \n" + forecast + "\n" + "Be as concise as possible. Answer in less than 200 characters."

        
        prompt = {
            "system": system,
            "user": user
        }

        response = self.call_api(prompt)


        return response


    def advice_style(self, forecast):

        system = "You are a personal assistant that adapts weather reports to the user's needs. Use more casual language - you aren't a weather reporter, you're a PA. Answer very concisely and in less than 200 characters."
        user = forecast + "\n" + "Provide your answer in the following format: 'Will it rain? <Answer> Wear a <Clothing> because <Reason>.'"

        prompt = {
            "system": system,
            "user": user
        }

        response = self.call_api(prompt)


        return response





class Weather:
    def __init__(self):
        pass

    def update(self, source_url):

        # Get forecast data from Met Office API
        data = requests.get(source_url).text
        data = json.loads(data)

        # # Save forecast data to debug file
        # with open("debug.json", "w") as write_file:
        #     json.dump(data, write_file, indent=4)

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

        current_path = os.getcwd()
        with open(current_path + "/files/params.json", "r") as f:
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

    def generate_report(weather):
        timenow = datetime.now()

        observed = weather.update(OBSERVED_24HOURS)
        observed = {key: value for key,
                    value in observed.items() if key.hour % 3 == 0}

        if timenow.hour < 12:
            observed = {key: value for key, value in observed.items() if key <
                        timenow.replace(hour=21, minute=0, second=0) - timedelta(days=1)}
        elif timenow.hour >= 12:
            observed = {key: value for key, value in observed.items() if key >
                        timenow.replace(hour=5, minute=59, second=59)}

        observed_strings = weather.weather_to_strings(observed)

        forecast = weather.update(FORECAST_5DAYS)
        forecast = {key: value for key, value in forecast.items() if key >
                    timenow - timedelta(hours=3)}
        forecast = {key: value for key, value in forecast.items() if key <
                    timenow.replace(hour=23, minute=59, second=59)}

        forecast_strings = weather.weather_to_strings(forecast)

        prompt = [
            "Past:",
            *observed_strings,
            "Future forecast:",
            *forecast_strings,
        ]

        return '\n'.join(prompt)

    def random_style(self):
        # Function to return random (style_name, style_description) from styles.csv

        with open(current_path + "/files/styles.csv", "r") as f:
            styles = list(csv.reader(f))
        style = choice(styles)
        return style
