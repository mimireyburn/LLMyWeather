from flask import Flask, render_template
from json import dump
from weather import Weather, OpenAI
from markupsafe import Markup
import imgkit


app = Flask(__name__)


@app.route("/")
def home():

    # Create dict
    output = {}

    # Get forecast data from Met Office API
    weather = Weather()
    weather_report = weather.generate_report()
    output["weather_report_prompt"] = weather_report

    # Summarise forecast with ChatGPT
    LLM = OpenAI()
    forecast = LLM.summarise_forecast(weather_report)
    output["forecast"] = forecast

    # Change style of forecast reporting with ChatGPT
    style = weather.random_style()
    style_name, style_desc = style[0], style[1]
    style_desc = "a poet who only writes weather-related haikus"
    output["style"] = style_name
    prompt, stylecast = LLM.change_style(forecast, style_desc)
    output["style_prompt"] = prompt
    output["stylecast"] = Markup(stylecast.replace("\n", "<br>"))

    # Write to json file for debugging
    with open("debug.json", "w") as write_file:
        dump(output, write_file, indent=4)

    # Read from json file for debugging
    # with open("debug.json", "r") as read_file:
    #     output = read_file.read()

    # Render render template

    rendered_render = render_template(
        "render.html", output=output)

    # Write to html file for static hosting
    with open("render.html", "w") as write_file:
        write_file.write(rendered_render)

    # Render screen template
    rendered_screen = render_template(
        "screen.html", output=output)

    # Write to html file for static hosting
    with open("screen.html", "w") as write_file:
        write_file.write(rendered_screen)

    options = {
        "enable-local-file-access": None,
        "height": 300,
        "width": 400
    }

    # Convert html to image
    print(output["stylecast"])
    imgkit.from_file('screen.html', 'out.png', options=options)

    # Return rendered template for local hosting
    return rendered_render


if __name__ == "__main__":
    app.run(debug=True)
