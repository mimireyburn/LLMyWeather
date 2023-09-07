# main.py
from weather import Weather, OpenAI
from visualise import Visualise
import time

WIDTH = 400
HEIGHT = 300
color = "yellow"

visualise = Visualise(WIDTH, HEIGHT)

if __name__ == "__main__":
    while True:
        # Create dict
        output = {}

        # Get forecast data from Met Office API
        weather = Weather()
        weather_report = weather.generate_report()

        # Summarise forecast with ChatGPT
        LLM = OpenAI()
        forecast = LLM.summarise_forecast(weather_report)
        output["forecast"] = forecast

        # Change style of forecast reporting with ChatGPT
        style = weather.random_style()
        style_name, style_desc = style[0], style[1]
        output["style"] = style_name
        stylecast = LLM.change_style(forecast, style_desc)
        output["stylecast"] = stylecast

        print(stylecast)

        result = style_name + ": \n" + stylecast

        # Render on e-ink display
        visualise.draw(stylecast, style_name)
        visualise.display(color)

        time.sleep(60)



