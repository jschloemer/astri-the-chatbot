# Created as an example to try catagorization via openai
# Author: Jeff Schloemer
# Date: 01/09/2023

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
    
    init="Extract acronym data from sentences and return in as pairs in comma seperated form. \nPrompt: The design concept (DC) that followed is based at the commercial available CubeSat structures; an aluminum frame consisting of four rails and four square parts surrounded by four sides.\nA: DC: design concept\n\nPrompt: The science unit (SU) is the primary payload of UPSat. It is provided from the QB50 program and it’s the multi-Needle Langmuir Probe (m-NLP) type. It has 4 probes that are deployed after the UPSat launch from ISS. SU communicates with the OBC through a serial connection. The OBC is responsible for sending commands to the SU and saving the SU information to the OBC’s mass storage. IAC - The IAC or Image Acquisition Component is the secondary payload of UPSat, defined from the university of Patras. \nA: SU: science unit, m-NLP: multi-Needle Langmuir Probe, IAC: Image Acquisition Component \n\nPrompt: "
    text2="Total Ionisation Dose (TID) refers to the cumulative effects of radiation in space, resulting in gradual degradation in operational parameters in electronics [52]. This affects missions with longer duration than a typical CubeSat in LEO. Single event effects or SEEs are separated into different groups and it can be transient or permanent:"
    prompt=text2
    fin = "\nA:"
    total = init + prompt + fin
    #print(total)
    ops = True
    
    if (ops):
        response = openai.Completion.create(
                    model="text-curie-001",
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