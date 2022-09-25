import json 
import requests
import os

KEY = os.environ['MET_OFFICE_API']
# print(os.environ)

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

# with open('test.json') as fp:
#     data = json.load(fp)


# westminster = 354160
# orkney = 353745

data = requests.get("http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/353745?res=3hourly&key=" + KEY).text
data = json.loads(data)

today = data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"]
today.pop(0)

mydict = {"rainy":{"ID": "Pp", "maximum_impact": 100, "zero_impact": 0, "weight":1},
    "windy":{"ID": "S", "maximum_impact":30, "zero_impact": 0, "weight": 0.6},
    "hot":{"ID": "F", "maximum_impact":40, "zero_impact":20, "weight":0.7},
    "cold":{"ID": "F", "maximum_impact":-5, "zero_impact":20, "weight":0.7}}

periods = {"0": "at night", "180": "early morning", "360": "in the morning", "540": "late morning", "720": "early afternoon", "900": "late afternoon", "1080": "in the evening", "1260": "late evening"}


output = {}

for window in today:

    # print(periods[window["$"]])

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
        # print("Weather type: ", weather_type, "Value: ", val, "Importance: ", norm)
        # print(descr[norm])

        statement = str(descr[norm] + " " + weather_type + " " + periods[window["$"]])

        output[statement] = norm * weight

    # print("______")

# print(output)
sorted_output = sorted(output.items(), key=lambda x: x[1], reverse=True)
# print(sorted_output)

# sorted_output = list(reversed(sorted(output.items())))
# print(sorted_output[0:3])

for item in sorted_output[0:3]: 
    print(item[0])

    # precip = window[params["Precip"]["ID"]]
    # wind = window[params["Wind"]["ID"]]
    # temp = window[params["Temp"]["ID"]]

    # print(precip, temp, wind)

  