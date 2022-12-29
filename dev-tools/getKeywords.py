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

# Extract the nouns from the document
nouns = [token.text for token in doc if token.pos_ == 'NOUN']
unique_nouns = sorted(set(nouns))

with open('nouns.txt', 'w') as f:
    for noun in unique_nouns:
        f.write("- search [" + noun + '](query)\n')
