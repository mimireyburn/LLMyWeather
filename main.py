# main.py
from weather import Weather, OpenAI

if __name__ == "__main__":
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
