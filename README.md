# WTHR

WTHR is an application for summarising weather data in a single sentence, using LLMs.

- Pulls live data from the UK Met Office API
- Summarises data with gpt-3.5-turbo API
- Option to apply 200+ ridiculous reporter 'styles'!

<img width="692" alt="Weather_1a" src="https://user-images.githubusercontent.com/32883278/235817723-427993ca-1077-44bf-bf9b-4f0aac88f900.png">

## Usage

Clone the repository:

```bash
git clone https://github.com/mimireyburn/WTHR.git
```

Install Flask, a lightweight web application framework for developing your site locally:

```bash
pip install Flask
```

Install Requests, a Python library for making HTTP requests to the APIs.

```bash
pip install requests
```

Do not edit `static/index.html`, it will be overwritten by the dynamic generation in `app.py`.

Run `app.py` to call the APIs and visualise the screen (generated using [Jinja2](https://palletsprojects.com/p/jinja/) in `templates/timeline.html`).

You should be able to view the screen at `http://127.0.0.1:5000`.

Edit the visualisation in `templates/base.html`. Saving the file should automatically refresh `http://127.0.0.1:5000`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
