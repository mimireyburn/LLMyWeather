from flask import Flask, render_template
from json import dump
from requests import get
from weather import Weather, OpenAI

app = Flask(__name__)


@app.route("/")
def home():

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

    # Write to json file for debugging
    with open("debug.json", "w") as write_file:
        dump(output, write_file, indent=4)

    # Render template
    rendered_output = render_template(
        "template.html", output=output)

    # Write to html file for static hosting
    with open("index.html", "w") as write_file:
        write_file.write(rendered_output)

    # Return rendered template for local hosting
    return rendered_output


if __name__ == "__main__":
    app.run(debug=True)
