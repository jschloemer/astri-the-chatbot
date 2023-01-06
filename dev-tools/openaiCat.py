# Created as an example to try catagorization via openai
# Author: Jeff Schloemer
# Date: 01/04/2023

# First, we need to install the elasticsearch and requests libraries:
#!pip install requests openai bs4

import openai
from bs4 import BeautifulSoup
import requests
import argparse
import os
import re

# Use the argparse library to parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('url', help='The URL with data to catagorize')
args = parser.parse_args()
url = args.url

# Setup OPENAI access
key = os.getenv("OPENAI_API_KEY")
useopenai = ""
if (key is None):
    useopenai = False
    print("No OPENAI API Key Found - All external queries will be stopped")
    exit()
else:    
    openai.api_key = key
    useopenai = True
    
if (useopenai):
    # Retrieve the HTML from the URL
    r = requests.get(url)
    html = r.text
    
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract the text content
    text2 = soup.get_text()
    text2 = str(text2)
    text2 = re.sub(r'\s\s+', '. ', text2)
    #print(text2)
    #print("=============================")
    
    init="Extract multi-word adjective and noun phrases from text and return them in a comma seperated list. Do not include single words\nPrompt: The design concept that followed is based at the commercial available CubeSat structures; an aluminum frame consisting of four rails and four square parts surrounded by four sides.\nA: design concept, commercial available CubeSat structures, alumninum frame, four rails, four square parts, four sides\n\nPrompt: The basic reason for following this road is the mass saving and secondly the very good mechanical properties the Composite Materials offer. Finding the best lamination for the Composite sides the structure can withstand the applied loads at all three axes as verified via Finite Element Analysis.  \nA: basic reason, mass saving, very good mechanical properties, Composite Materials, best lamination, Composite sides, applied loads, three axes, Finite Element Analysis \n\nPrompt: "
    prompt=text2
    fin = "\nA:"
    total = init + prompt + fin
    #print(total)
    ops = True
    
    if (ops):
        response = openai.Completion.create(
                    model="text-babbage-001",
                    prompt=total,
                    temperature=0,
                    max_tokens=300,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stop=["\n"]
                )
        print(response)
        #print(response['choices'][0]['text'])
        output = response['choices'][0]['text']
        
        stringList = output.split(',')
        for line in stringList:
            print('- ' + line)
        
        