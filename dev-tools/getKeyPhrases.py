# Author: Jeff Schloemer
# Date: 12/29/2022

import requests
from bs4 import BeautifulSoup
import spacy

# Send a GET request to the webpage
response = requests.get('https://nchronas.github.io/upsat_msc_thesis/')

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the elements that contain text on the page
text_elements = soup.find_all(text=True)

# Extract the text from the elements
text = ' '.join(text_elements)

# Load the spacy model
nlp = spacy.load('en_core_web_sm')

# Parse the text using the spacy model
doc = nlp(text)

# Extract the adjective and verb phrases from the document
phrases = []
for token in doc:
    if token.pos_ == 'ADJ' or token.pos_ == 'VERB':
        phrase = ''
        for t in token.subtree:
            phrase += t.text + ' '
        phrases.append(phrase.strip())

# Remove duplicates and sort the phrases
unique_phrases = sorted(set(phrases))

# Write the phrases to a file
with open('phrases.txt', 'w') as f:
    for phrase in unique_phrases:
        f.write("- search [" + phrase + '](query)\n')        
