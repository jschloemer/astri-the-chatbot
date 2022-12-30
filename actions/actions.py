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

# Part Items
import pandas as pd

# Setup the part data
useacronyms = False
try:
    # Load the JSON file into a pandas DataFrame
    df = pd.read_json('index/acronyms.json')
    # Convert the strings in the 'Entity' column to lowercase
    df['Acronym'] = df['Acronym'].str.lower()

    # Print the DataFrame
    print(df)
    useacronyms = True
except:
    useacronyms = False
    print("No Acronym Data Found")

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
        
        prompt = tracker.get_slot("prompt")
        print(prompt)
        
        text = "Prompt: " + str(prompt)
        dispatcher.utter_message(text=text)
        
        if (useopenai and prompt is not None):
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
        return [SlotSet("query", None), SlotSet("project", None)]

class ActionResetPartSlot(Action):
    
    def name(self) -> Text:
        return "action_reset_part_slot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("part", None)]
    
class ActionResetPromptSlot(Action):
    
    def name(self) -> Text:
        return "action_reset_prompt_slot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("prompt", None)]
        
class ActionPerformSearch(Action):

    def name(self) -> Text:
        return "action_perform_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Performing Search")
        
        query = tracker.get_slot('query')
        project = tracker.get_slot('project')
        
        text = "Query: " + str(query) + " Project: " + str(project)
        
        dispatcher.utter_message(text=text)

        return []
    
class ActionLookupPart(Action):

    def name(self) -> Text:
        return "action_lookup_part"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Looking up part")
        
        part = tracker.get_slot('part')
        text = "Got it! Part: " + str(part)
        dispatcher.utter_message(text=text)
        
        print(str(part))
        
        numResponses = 0
        
        entityFilled = True
        
        if (part is None or part == ""):
            entityFilled = False
            text = "Passed search string was blank. Sorry!!"
            dispatcher.utter_message(text=text)

        if (useacronyms or entityFilled is False):
            # Find the entity in the 'Acronym' column
            entity = part

            try:
                # Return the item in the 'Item' column
                item = df.loc[df['Acronym'] == entity.lower(), 'Description'].values[0]

                #print(item)  # Output: 'Item 1'
                
                # Create the response
                text = str(entity) + " stands for " + str(item)
                numResponses = numResponses + 1
                dispatcher.utter_message(text=text)
            except:
                print("No Acronym Match Found")
        
        if (numResponses == 0):
            text = "After reviewing the documentation, no information was found. Sorry."
            dispatcher.utter_message(text=text)
        
        return []
