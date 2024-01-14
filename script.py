# Telethon utility #pip install telethon
import configparser  # Library for reading from a configuration file, # pip install configparser
import datetime  # Library that we will need to get the day and time, #pip install datetime
import random  # pip install random
from random import randint

import requests  # Library used to make requests to external services (the weather forecast one) # pip install requests
from telethon import TelegramClient, events
from telethon.tl.custom import Button

#### Access credentials
config = configparser.ConfigParser()  # Define the method to read the configuration file
config.read('config.ini')  # read config.ini file

api_id = config.get('default', 'api_id')  # get the api id
api_hash = config.get('default', 'api_hash')  # get the api hash
BOT_TOKEN = config.get('default', 'BOT_TOKEN')  # get the bot token
weather_key = config.get('default', 'weather_key')  # read the key for the weather forecasts
nutrition_key = config.get('default', 'nutrition_key')
aqi_key = config.get('default', 'aqi_key')
bmi_key = config.get('default', 'bmi_key')
exercise_key = config.get('default', 'exercise_key')
# Create the client and the session called session_master. We start the session as the Bot (using bot_token)
client = TelegramClient('sessions/session_master', api_id, api_hash).start(bot_token=BOT_TOKEN)

# Define the /start command
@client.on(events.NewMessage(pattern='(?i)/start'))
async def start(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = "Hello, i am Medico bot made by Mrigank. Lets start the fun. Press the following blue links.\n" + \
           "\"<b>/weather CITY</b>\" → I will provide the weather forecast for the city you entered\n" + \
           "\"<b>/nutrition</b>\" → Let's eat healthy together!\n" + \
           "\"<b>/aqi</b>\" → Find out what aqi it is!\n" + \
           "\"<b>/bmi</b>\" → I will provide the bmi for your weight(kg) and height(m)\n" + \
           "\"<b>/exercise</b>\" → I will provide the exercises\n"

    await client.send_message(SENDER, text, parse_mode="HTML")

### Command to get the weather
@client.on(events.NewMessage(pattern='(?i)/weather'))
async def weather(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id

    try:
        msg = event.message.text
        after_command = msg.split(" ")[1:]
        city = ' '.join(after_command)

        url = "https://weather-api-by-any-city.p.rapidapi.com/weather/"+city
        headers = {
            "X-RapidAPI-Key": "123",
            "X-RapidAPI-Host": "weather-api-by-any-city.p.rapidapi.com"
        }
        json_response = requests.get(url, headers=headers)
        json_weather = json_response.json()

        temp= json_weather['current']['temp_c']
        text= json_weather['current']['condition']['text']
        mssg= "Temperature is " + str(temp) + "C and it is " + text
        await client.send_message(SENDER, mssg, parse_mode="HTML")

    except:
        await client.send_message(SENDER, "Insert city name after the /weather command!", parse_mode="HTML")
        return

    ## Function that waits user event [press button]



### Command to get the nutrition
@client.on(events.NewMessage(pattern='(?i)/nutrition'))
async def nutrition(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id

    try:
        msg = event.message.text
        after_command = msg.split(" ")[1:]
        food = ' '.join(after_command)

        # Define the URL to make the request
        base_url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"

        # Get response and parse it to JSON format
        querystring = {"query": food}
        headers = {
            "X-RapidAPI-Key": "123",
            "X-RapidAPI-Host": "nutrition-by-api-ninjas.p.rapidapi.com"
        }
        json_response = requests.get(base_url, headers=headers, params=querystring)
        json_nutrition = json_response.json()

        calories = json_nutrition[0]['calories']
        fat_total_g= json_nutrition[0]['fat_total_g']
        protein_g = json_nutrition[0]['protein_g']
        sugar_g = json_nutrition[0]['sugar_g']

        mssg= "Calories: "+str(calories) +" , Total fat: "+str(fat_total_g) +" , Protein: "+str(protein_g) +" , Sugar: "+str(sugar_g)
        await client.send_message(SENDER, mssg, parse_mode="HTML")

    except:
        await client.send_message(SENDER, "Insert food name after the /nutrition command!", parse_mode="HTML")
        return

    ## Function that waits user event [press button]


### Command to get the air-quality-index
@client.on(events.NewMessage(pattern='(?i)/aqi'))
async def aqi(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id

    try:
        msg = event.message.text  # /weather new york
        after_command = msg.split(" ")[1:]  # ['/weather', 'new', 'york']
        city = ' '.join(after_command)  # we get 'new york'

        # Define the URL to make the request
        base_url = "https://air-quality-by-api-ninjas.p.rapidapi.com/v1/airquality"

        querystring = {"city": city}

        headers = {
            "X-RapidAPI-Key": "123",
            "X-RapidAPI-Host": "air-quality-by-api-ninjas.p.rapidapi.com"
        }

        json_response = requests.get(base_url, headers=headers, params=querystring)
        json_aqi = json_response.json()

        aqi = json_aqi['overall_aqi']
        messg = "The aqi of " + str(city) + " is " + str(aqi)
        # c_text = "Calories of " + food + " is <b>" + str(calories)
        await client.send_message(SENDER, messg, parse_mode="HTML")

    # If the user just send the /weather commandi without a CITY, we get and Exeption
    except:
        await client.send_message(SENDER, "Insert city name after the /aqi command!", parse_mode="HTML")
        return


### Command to get the exercise
@client.on(events.NewMessage(pattern='(?i)/exercise'))
async def exercise(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id

    try:
        msg = event.message.text  # /weather new york
        after_command = msg.split(" ")[1:]  # ['/weather', 'new', 'york']
        exercisetype = after_command[0]  # we get 'new york'
        difficulty = after_command[1]

        # Define the URL to make the request
        url = "https://exercises-by-api-ninjas.p.rapidapi.com/v1/exercises"
        querystring = {"type": "cardio", "difficulty": "beginner"}
        headers = {
            "X-RapidAPI-Key": "123",
            "X-RapidAPI-Host": "exercises-by-api-ninjas.p.rapidapi.com"
        }
        json_response = requests.get(url, headers=headers, params=querystring)
        json_exercise = json_response.json()

        await client.send_message(SENDER,  json_exercise[0]['instructions'], parse_mode="HTML")
        await client.send_message(SENDER,  json_exercise[1]['instructions'], parse_mode="HTML")

    # If the user just send the /weather commandi without a CITY, we get and Exeption
    except:
        await client.send_message(SENDER, "Enter exercise type and difficulty level after the /exercise command!", parse_mode="HTML")
        return

def press_event(user_id):
    return events.CallbackQuery(func=lambda e: e.sender_id == user_id)


### Command to get the bmi
@client.on(events.NewMessage(pattern='(?i)/bmi'))
async def bmi(event):
    # Get the sender of the message
    sender = await event.get_sender()
    SENDER = sender.id

    try:
        msg = event.message.text  # /weather new york
        after_command = msg.split(" ")[1:]  # ['/weather', 'new', 'york']
        weight = after_command[0]  # we get 'new york'
        height = after_command[1]

        # Define the URL to make the request
        url = "https://body-mass-index-bmi-calculator.p.rapidapi.com/metric"
        querystring = {"weight": weight, "height": height}
        headers = {
            "X-RapidAPI-Key": "123",
            "X-RapidAPI-Host": "body-mass-index-bmi-calculator.p.rapidapi.com"
        }

        json_response = requests.get(url, headers=headers, params=querystring)
        json_bmi = json_response.json()

        bmi = json_bmi['bmi']
        if bmi<18.5:
            message = "you are underweight and health risk is minimal"
        elif bmi>=18.5 and bmi<=24.9:
            message = "you are normal and health risk is minimal"
        elif bmi>=25 and bmi<=29.9:
            message = "you are overweight and health risk is increased"
        elif bmi>=30 and bmi<=34.9:
            message = "you are obese and health risk is high"
        elif bmi>=35 and bmi<=39.9:
            message = "you are severely obese and health risk is very high"
        else:
            message = "you are morbidily obese and health risk is extremely high"

        mssg= "Your BMI is: " + str(bmi) + " & " + message
        # c_text = "Calories of " + food + " is <b>" + str(calories)
        await client.send_message(SENDER, mssg, parse_mode="HTML")

    except:
        await client.send_message(SENDER, "Insert weight and height after the /bmi command!", parse_mode="HTML")
        return

def press_event(user_id):
    return events.CallbackQuery(func=lambda e: e.sender_id == user_id)

    ### MAIN

if __name__ == '__main__':
    print("bot started")
    client.run_until_disconnected()
