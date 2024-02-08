# LLMyWeather

LLMyWeather is an application for summarising weather data in a single sentence, using LLMs.

- Pulls live data from the UK Met Office API
- Summarises data with gpt-3.5-turbo API
- Option to apply 200+ ridiculous reporter 'styles'!

<img src="https://github.com/mimireyburn/LLMyWeather/assets/79009541/cb5bd7a6-c450-4b72-8a25-78584b7b6613" width="600">

## Usage

Clone the repository:

```bash
git clone https://github.com/mimireyburn/LLMyWeather.git
```

Create a **keys.py** file based on keys_example.py. You will need: 

1. **OpenAI API Key**
2. **MET Office DataPoint API Key**   
3. **DataPoint Location ID** (e.g. Cambridge is *310042*)
4. **MET Office Observed Location ID** (Not all weather stations report historical data to the API - test it first. e.g. Heathrow works and is *3772*)
5. **MET Office Historical Location** (e.g. *England_SE_and_Central_S*)


You can find the DataPoint API reference [here](https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/data/datapoint_api_reference.pdf). To use it, register for a [free API key](https://www.metoffice.gov.uk/services/data/datapoint/api).


### Running on Raspberry Pi with InkyWHAT

<img width="692" alt="InkyWeather" src="https://github.com/mimireyburn/LLMyWeather/assets/79009541/2e6acc9e-8c87-4baf-b760-55d5a9ab6fdc">

At the top of the **main.py** file, change the following lines to match your setup:

```python
# Dimensions and colour of the InkyWHAT display
WIDTH = 400
HEIGHT = 300
COLOUR = "yellow"
# Frequency of display refresh in minutes
UPDATE_BUFFER = 60
# Define delivery style.
SYSTEM = "assistant" # or "entertainer"
```

The *Assistant* persona acts as a PA, delivering the weather forecast with some advice on what to wear or bring with you. The *Entertainer* persona is a bit more fun, delivering the weather forecast in a random style from a list of 200+ ridiculous reporters. If unspecified, the default is *Weather Reporter*.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
