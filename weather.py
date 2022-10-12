import json 
import requests
import os

class Weather(object):
    def __init__(self, key, location):
        self.key = key
        self.location = location


    def update(self):
        descr = {
            0 : "not",
            1 : "a tiny bit",
            2 : "slightly",
            3 : "fairly",
            4 : "a bit",
            5 : "quite",
            6 : "very",
            7 : "o shit it's",
            8 : "extremely",
            9 : "disgustingly",
            10: "FUCKIN"
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

                norm = (val - zero_impact)/(maximum_impact - zero_impact) * 10
                weight = mydict[weather_type]["weight"]

                norm = abs(round(norm))

                statement = str(descr[norm] + " " + weather_type + " " + periods[window["$"]])

                output[statement] = norm * weight

        sorted_output = sorted(output.items(), key=lambda x: x[1], reverse=True)

        results = []
        for item in sorted_output[0:3]: 
            results.append(item[0])
        
        return results

