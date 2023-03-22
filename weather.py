import json 
import requests
import os
import openai
import random

class Weather(object):
    def __init__(self, key, location, openai_key):
        self.key = key
        self.location = location
        self.openai_key = openai_key

    def update(self):

        descr = {
            0.0 : ["not", "not even a little", "never"],
            0.1 : ["a tiny bit", "a tad", "a wee bit"],
            0.2 : ["a touch", "slightly", "you could say it is"],
            0.3 : ["just a bit", "kinda", "sort of"],
            0.4 : ["a bit", "pretty", "a good bit"],
            0.5 : ["quite", "partly", "fairly"],
            0.6 : ["very", "mostly", "getting pretty"],
            0.7 : ["oh shit it's", "oh boy, it's", "heckin'"],
            0.8 : ["extremely", "awfully", "wildly"],
            0.9 : ["disgustingly", "exceptionally", "overwhelmingly"],
            1.0 : ["FUCKING", "unbelievably", "insanely"]
        }

        mydict = {
            "rainy":{
                "ID": "Pp",
                "maximum_impact": 100,
                "zero_impact": 0,
                "weight":1
                },
            "windy":{
                "ID": "S",
                "maximum_impact":30,
                "zero_impact": 0,
                "weight": 0.6
                },
            "hot":{
                "ID": "F",
                "maximum_impact":40,
                "zero_impact":20,
                "weight":0.7
                },
            "cold":{
                "ID": "F",
                "maximum_impact":-5,
                "zero_impact":20,
                "weight":0.7
            }
        }

        periods = {
            "0": "at night", 
            "180": "early morning", 
            "360": "in the morning", 
            "540": "late morning", 
            "720": "early afternoon", 
            "900": "late afternoon", 
            "1080": "in the evening", 
            "1260": "late evening"
        }

        weather_code = { 
            "0" : ["Clear night", 0],
            "1" : ["Sunny day", 0.8],
            "2" : ["Partly cloudy (night)",  0],
            "3" : ["Partly cloudy (day)",  0],
            "4" : ["Not used", 0],
            "5" : ["Mist", 1],
            "6" : ["Fog", 1],
            "7" : ["Cloudy", 0.1],
            "8" : ["Overcast", 0.3],
            "9" : ["Light rain shower (night)", 0.4],
            "10": ["Light rain shower (day)", 0.4],
            "11": ["Drizzle", 0.4],
            "12": ["Light rain", 1],
            "13": ["Heavy rain shower (night)", 1],
            "14": ["Heavy rain shower (day)", 1],
            "15": ["Heavy rain", 1],
            "16": ["Sleet shower (night)", 1],
            "17": ["Sleet shower (day)", 1],
            "18": ["Sleet", 1],
            "19": ["Hail shower (night)", 1],
            "20": ["Hail shower (day)", 1],
            "21": ["Hail", 1],
            "22": ["Light snow shower (night)", 1],
            "23": ["Light snow shower (day)", 1],
            "24": ["Light snow", 1],
            "25": ["Heavy snow shower (night)", 1],
            "26": ["Heavy snow shower (day)", 1],
            "27": ["Heavy snow", 1],
            "28": ["Thunder shower (night)", 1],
            "29": ["Thunder shower (day)", 1],
            "30": ["Thunder", 1]
        }

        random_word = ["british", "sarcastic", "rude", "foul-mouthed", ""]
        format = ["rap about today's weather forecast", "rhyming poem for the weather forecast", "weather forecast", "summary of the upcoming weather", "sentence about today's weather", "weather forecast in the style of Master Yoda"]


        data = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/" + self.location + "?res=3hourly&key=" + self.key).text
        data = json.loads(data)

        today = data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"]
        today.pop(0)

        output = {}

        for window in today: 
            for weather_type in mydict.keys():
                id = mydict[weather_type]["ID"]
                val = int(window[id])
                    
                zero_impact = mydict[weather_type]["zero_impact"]
                maximum_impact = mydict[weather_type]["maximum_impact"]

                if maximum_impact < zero_impact:
                    val = min(max(val, maximum_impact), zero_impact)
                else:
                    val = max(min(val, maximum_impact), zero_impact)

                norm = ((val - zero_impact)/(maximum_impact - zero_impact))
                weight = mydict[weather_type]["weight"]

                norm = abs(round(norm, 1))

                statement = str(descr[norm][random.randint(0,2)] + " " + weather_type + " " + periods[window["$"]])
                output[statement] = norm * weight

                #  get weather_code statement 
                weather_code_info = weather_code[window["W"]]
                output[weather_code_info[0] + " " + periods[window["$"]]] = weather_code_info[1]

                
        sorted_output = sorted(output.items(), key=lambda x: x[1], reverse=True)
        results = []

        for item in sorted_output[0:5]: 
            results.append(item[0])

        results = ', '.join(results)

        adjective = random_word[random.randint(0,len(random_word)-1)]

        forecast_format = format[random.randint(0, len(format)-1)]

        prompt = "Write a " + adjective + " " + forecast_format + " from this prompt: " + results

        openai.api_key = self.openai_key
        response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=128,
        top_p=1,
        frequency_penalty=1.7,
        presence_penalty=1.0
        )

        print("PROMPT:", prompt)
        print(response["choices"][0]["text"])

        return response

