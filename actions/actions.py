# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet

# Search Items

import elasticsearch
import openai
import os

# Setup for openai access
## If not setup, set global boolean to prevent errors
key = os.getenv("OPENAI_API_KEY")
useopenai = ""
if (key is None):
    useopenai = False
    print("No OPENAI API Key Found - All external queries will be stopped")
else:    
    openai.api_key = key
    useopenai = True
useopenai = False

class ActionSendAIGen(Action):
    
    def name(self):
        return "action_send_ai_gen"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if (useopenai and prompt is not None):
            prompt = tracker.get_slot("prompt")
            print(prompt)
            init="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with Unknown.\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: "
            fin = "?\nA:"
            dispatcher.utter_message(text="Looking up this question")
            
            total = init + prompt + fin
 
            
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=total,
                temperature=0.05,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["\n"]
            )
            
            if(response=="Unknown"):
                response = "Sorry, I don't know the answer to this one"
            
            dispatcher.utter_message(text=response)
        else:
            print(prompt)
            dispatcher.utter_message(text="Access to this information has not been setup properly. Sorry")
        
        return []

class ActionResetAllSlots(Action):

    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]

class ActionResetSearchSlot(Action):
    
    def name(self) -> Text:
        return "action_reset_search_slot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tracker.update_slot("query", None)
        tracker.update_slot("project", None)
        return []

class ActionResetPartSlot(Action):
    
    def name(self) -> Text:
        return "action_reset_part_slot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tracker.update_slot("part", None)
        return []
    
class ActionResetPromptSlot(Action):
    
    def name(self) -> Text:
        return "action_reset_prompt_slot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tracker.update_slot("prompt", None)
        return []
        
class ActionPerformSearch(Action):

    def name(self) -> Text:
        return "action_perform_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Performing Search")

        return []
    
class ActionLookupPart(Action):

    def name(self) -> Text:
        return "action_lookup_part"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Looking up part")

        return []
