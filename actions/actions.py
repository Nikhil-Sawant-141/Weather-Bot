# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests


class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        api_key = '...' ### your api key

        loc = tracker.get_slot("location")
        parameters = {
            'access_key': api_key,
            'query': loc
        }

        current = requests.get('http://api.weatherstack.com/current', params=parameters)

        result = current.json()

        if "current" in result.keys():

            country = result['location']['country']
            city = result['location']['name']
            condition = result['current']['weather_descriptions'][0]
            temperature = result['current']['temperature']
            humidity = result['current']['humidity']
            wind_speed = result['current']['wind_speed']
            icon = result['current']['weather_icons'][0]

            response = """It is currently {} in {},{} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(
                condition, city, country, temperature, humidity, wind_speed)

            dispatcher.utter_message(response)
            dispatcher.utter_message(image=icon)
        else:
            dispatcher.utter_message("""Sorry, I cannot provide weather details for {}. Please enter a valid city or country name.""".format(loc))

        return [SlotSet("location", loc)]
