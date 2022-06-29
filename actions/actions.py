import datetime as dt
import requests
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"I'll see if I can get you an answer. This might take a while. Don't hang up on me.")

        # url = "https://api.eu1.robocorp.com/process-v1/workspaces/e1d0e43f-0ba4-4f7d-ae19-53f49cfe03f8/processes?"
        url = "https://api.eu1.robocorp.com/process-v1/workspaces/e1d0e43f-0ba4-4f7d-ae19-53f49cfe03f8/processes/033cbdd0-6edc-4d15-8869-025b83bbf2a3/run-request?"
        data = {'type': 'default'}
        headers = {"Authorization": "RC-WSKEY 2HVY8PrMQedcYPSSiZUaG0M4cePmCICw00g4Odx7y8zTTTU4bxD3IOgoVUWjv9RHtVvk074Fam6dnAYJpqtiacxyFMgB7d1Jwq1KrQwXhhh7THEgiY06STVghSj0NuDO"}

        r = requests.post(url, json=data, headers=headers)

        userid = tracker.current_state()['sender_id']

        dispatcher.utter_message(f"Entities: {tracker.latest_message.get('text')}")
        city = tracker.get_slot("GPE")
        dispatcher.utter_message(f"Entity value is {city}!")

        dispatcher.utter_message(text=f"It's {dt.datetime.now()} on my machine and your are {userid}. Response from Robocorp: {r.text}")

        return []
