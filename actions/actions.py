import requests
import spacy
import settings
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"Right! This might take a while as I'll open a browser and check google for you. Don't hang up on me.")

        userid = tracker.current_state()['sender_id']

        # This is where the city SHOULD come.
        #city = tracker.get_slot("GPE")

        # This is simply to fix the broken env issue.
        nlp = spacy.load("en_core_web_md")
        doc = nlp(tracker.latest_message.get('text'))
        city = doc.ents[0]

        # ---- Start process with single work item payload
        
        # This is the right demo workspace
        url = "https://api.eu1.robocorp.com/process-v1/workspaces/d6b65aa4-0c45-4fd7-8bec-d68a29896e78/processes/a4fee379-ee93-4ce7-a64a-842c2677df43/runs?"
        headers = {"Authorization": settings.control_room_apikey}
         
        data = {
            "user": userid,
            "city": str(city) 
        }

        r = requests.post(url, json=data, headers=headers)

        dispatcher.utter_message(text=f"You are user {userid}. I've started a robot to get you an answer. Technical details here: {r.text}")

        return []

class ActionTellTime(Action):
    """Informs the user of the time results."""

    def name(self) -> Text:
        return "action_tell_time"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        time = next(tracker.get_latest_entity_values("timeresult"), "unknown time")
        city = next(tracker.get_latest_entity_values("cityresult"), "somewhere")

        dispatcher.utter_message(f"I've got your result! It is {time} in {city}.")

        return []