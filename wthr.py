import json 


with open('test.json') as fp:
    data = json.load(fp)


today = data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"]


mydict = {"Precip":{"ID": "Pp", "impact_max_positive": 100, "impact_zero": 0, "weight":1},
    "Wind":{"ID": "S", "impact_max_positive":50, "impact_zero": 0, "weight": 1},
    "Temp":{"ID": "F", "impact_max_positive":40, "impact_zero":16, "impact_max_negative":-5, "weight":1}}

periods = {"0": "night", "180": "early morning", "360": "morning", "540": "late morning", "720": "early afternoon", "900": "late afternoon", "1080": "evening", "1260": "late evening"}

# mydict = {"Temp":{"ID": "F", "impact_max_positive":40, "impact_zero":16, "impact_max_negative":-5, "weight":1}}

for window in today:

    print(periods[window["$"]])

    for weather_type in mydict.keys():
        id = mydict[weather_type]["ID"]
        val = int(window[id])

        impact_zero = mydict[weather_type]["impact_zero"]

        impact_max_positive = mydict[weather_type]["impact_max_positive"]
        val = min(val, impact_max_positive)

        try:
            impact_max_negative = mydict[weather_type]["impact_max_negative"]
            val = max(val, impact_max_negative)
        except KeyError:
            pass

        if val >= impact_zero:
            norm = round((val - impact_zero)/(impact_max_positive - impact_zero), 2) 
        else:
            norm = round((impact_zero - val)/(impact_zero - impact_max_negative), 2)

        print("Weather type: ", weather_type, "Value: ", val, "Importance: ", norm)
    print("______")

    # precip = window[params["Precip"]["ID"]]
    # wind = window[params["Wind"]["ID"]]
    # temp = window[params["Temp"]["ID"]]

    # print(precip, temp, wind)

