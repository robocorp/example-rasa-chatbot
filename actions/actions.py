import requests
import spacy
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

        userid = tracker.current_state()['sender_id']

        # This is where the city SHOULD come.
        #city = tracker.get_slot("GPE")

        # This is simply to fix the broken env issue.
        nlp = spacy.load("en_core_web_md")
        doc = nlp(tracker.latest_message.get('text'))
        city = doc.ents[0]

        # Start process with single work item payload
        url = "https://api.eu1.robocorp.com/process-v1/workspaces/d6b65aa4-0c45-4fd7-8bec-d68a29896e78/processes/29856e96-5153-4a9e-8c75-6dd4404cec43/runs?"
        data = {
            "user": userid,
            "city": str(city) 
        }
        headers = {"Authorization": "RC-WSKEY bfyDwf9ZAMI9ZBMsytqsBn5sGl01ADon9LcHeAAqFisfi716WpF0atZi4Az50ObPZc7haaRLICElRl0OYYOcM9TG5AXYDSQdIl8LI79Gkzx6YqyPcuehgDrjVWdKY"}

        r = requests.post(url, json=data, headers=headers)

        dispatcher.utter_message(text=f"You are user {userid}. I've started a robot to get you an answer. Technical details here: {r.text}")

        return []
