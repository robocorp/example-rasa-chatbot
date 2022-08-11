import requests
import spacy
import settings
from RPA.Robocorp.Process import Process
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text=f"Right! This might take a while as I'll open a browser and check google for you. Don't hang up on me.")

        userid = tracker.current_state()['sender_id']

        # This is where the city SHOULD come.
        #city = tracker.get_slot("GPE")

        # This is simply to fix the broken env issue.
        nlp = spacy.load("en_core_web_md")
        doc = nlp(tracker.latest_message.get('text'))
        city = doc.ents[0]

        # ---- Start process with single work item payload

        # Create work item payload
        data = {
            "user": userid,
            "city": str(city)
        }

        # Authenticate with Robocorp Control Room API
        process = Process(settings.workspace, settings.process, settings.apikey)
        r = process.start_process(data)

        dispatcher.utter_message(text=f"Right, {str(city)} it is. Hold on, robot is running!")

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
        city = next(tracker.get_latest_entity_values("cityresult"), "Somewhere")

        dispatcher.utter_message(f"I've got your result! It is {time} in {city}.")

        return []

class ActionTellError(Action):
    """Informs the user of the error in bot action."""

    def name(self) -> Text:
        return "action_tell_error"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        errortext = next(tracker.get_latest_entity_values("errortext"), "Undefined error.")
        city = next(tracker.get_latest_entity_values("cityresult"), "Somewhere")

        dispatcher.utter_message(f"Your bot run for {city} resulted in an error: {errortext}")

        return []

