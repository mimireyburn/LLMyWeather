import os
import time
# from visualise import Visualise
from weather import Weather
import openai

westminster = 354160
orkney = 353745
hammersmith = 351743

KEY = os.environ['MET_OFFICE_API']
OPENAI_KEY = os.environ["OPENAI_API_KEY"]
WIDTH = 400
HEIGHT = 300
LOCATION = str(hammersmith)

colour = "red"

if __name__ == "__main__":
    weather = Weather(KEY, LOCATION, OPENAI_KEY)
    # visualise = Visualise(WIDTH, HEIGHT)
    # while True:
    data = weather.update()
        # visualise.draw(data)
        # visualise.display(colour)
        # Update every 5 mins
        # time.sleep(300)

