import json
import requests
import openai
import keys

# MET OFFICE
MET_OFFICE_API_KEY = keys.MET_OFFICE_API_KEY
FORECAST_LOCATION = keys.FORECAST_LOCATION
FORECAST_FIVEDAYS = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"
FORECAST_RESOLUTION = "3hourly"
OBSERVED_LOCATION = keys.OBSERVED_LOCATION
OBSERVED_24HOURS = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/"
OBSERVED_RESOLUTION = "hourly"

# OPENAI
OPENAI_KEY = keys.OPENAI_API_KEY


class Weather(object):
    def __init__(self, MET_OFFICE_API_KEY, FORECAST_LOCATION, FORECAST_FIVEDAYS, OBSERVED_24HOURS, FORECAST_RESOLUTION):
        self.MET_OFFICE_API_KEY = MET_OFFICE_API_KEY
        self.FORECAST_LOCATION = FORECAST_LOCATION
        self.FORECAST_FIVEDAYS = FORECAST_FIVEDAYS
        self.OBSERVED_24HOURS = OBSERVED_24HOURS
        self.FORECAST_RESOLUTION = FORECAST_RESOLUTION

    def update(self):
        forecast = requests.get(
            FORECAST_FIVEDAYS + self.FORECAST_LOCATION + "?res=" + self.FORECAST_RESOLUTION + "&key=" + self.MET_OFFICE_API_KEY).text
        forecast = json.loads(forecast)
        past_24_hours = requests.get(
            OBSERVED_24HOURS + self.FORECAST_LOCATION + "?res=" + self.FORECAST_RESOLUTION + "&key=" + self.MET_OFFICE_API_KEY).text

        with open("debug_future.json", "w") as write_file:
            json.dump(forecast, write_file, indent=4)

        with open("debug_past.json", "w") as write_file:
            json.dump(past_24_hours, write_file, indent=4)

        # today = data["SiteRep"]["DV"]["FORECAST_Location"]["Period"][0]["Rep"]
        # today.pop(0)


if __name__ == "__main__":
    weather = Weather(MET_OFFICE_API_KEY, FORECAST_LOCATION,
                      FORECAST_FIVEDAYS, OBSERVED_24HOURS, FORECAST_RESOLUTION)
    weather.update()
