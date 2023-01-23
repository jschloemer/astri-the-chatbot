# Designed to be a standalone processor of project text. The goals as follows:
# - 1) Generate training data and test data to use for Rasa NLU from the core text
# - 2) Identify sentences with acroynms in them
# - 3) Attempt to create meaningful data relationships for easy lookup for Astri
# Author: Jeff Schloemer
# Date: 01/23/2023

import nltk
import argparse
import requests
import PyPDF2
import re
import random
from bs4 import BeautifulSoup

# Debug settings
debug = True

# Download the tokenizers and stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# Function for filtering sentences
def filter_sentences(sentences, min_length=3, max_length=25):
    # Initialize an empty list to store the filtered sentences
    n_sentences = []

    #iterate through the sentences and check if they meet the criteria
    for sentence in sentences:
        # Length criteria
        le = len(sentence.split())
        if le > min_length and le < max_length:
            n_sentences.append(sentence)
        
            
    s_sentences = []

    #iterate through the sentences and check if they contain stop words
    for sentence in n_sentences:
        words = set(sentence.split())
        if len(words.intersection(stop_words)) < len(words):
            s_sentences.append(sentence)

    # Return the filtered sentences
    return s_sentences

# Function for cleaning sentences
def clean_sentences(sentences):
    # Initialize an empty list to store the clean sentences
    c_sentences = []
    
    #iterate through the sentences and remove extra whitespace
    for sentence in sentences:
        # Length criteria
        w_text = re.sub(r'\s', ' ', sentence)
        p_text = w_text.rstrip("!.?;:")
        text = p_text.strip()
        c_sentences.append(text)
        
    return c_sentences

# Function for cleaning text
def clean_text(text):
    # Use a regular expression to remove whitespace
    i_text = re.sub(r'\s+', ' ', text)
    c_text = re.sub(r"[^\s\w!@#$5\^&*();:,./?\\<>{}\[\]\-\+=_`~]", ".", i_text)
    return c_text

# Function for parsing through clean sentences for NLU data
def create_NLU(sentences):
    # Create empty lists
    search_terms = []
    
    # Go through one sentence at a time
    for sentence in sentences:
        words = sentence.split()
        tot = len(words)
        while (tot > 0):
            pops = 0
            
            # Randomize how many words to bite off
            rand = random.randint(0, 99)
            if rand in range(0,40):
                pops = 1
            elif rand in range(40,70):
                pops = 2
            elif rand in range(70,85):
                pops = 3
            elif rand in range(85,95):
                pops = 4
            else:
                pops = 5
                
            # Check to see if pop are too many
            if pops > tot:
                pops = tot
                
            # Merge text together and add to list
            term = ""
            for i in range(pops):
                term = words.pop() + " " + term
            search_terms.append(term.strip())
            
            # Decrease the words remaining
            tot = len(words)
        
    # Clean and vett the terms
    
    # Remove duplicates
    u_search_terms = list(set(search_terms))
    
    # Clean list of search terms
    c_search_terms = []
    
    for term in u_search_terms:
        # clean out special characters
        c_term = re.sub(r"[^\s\w-]", "", term)
        
        # Check to see if it only stop words
        words = set(c_term.split())
        if len(words.intersection(stop_words)) < len(words):
            c_search_terms.append(c_term)
    
    # Check for dups again
    uc_search_terms = list(set(c_search_terms))
    
    # Output the data
    
    # Setup strings
    nlu_terms = ['search', 'search for', 'find']
    
    # Percent train
    train = 0.9
    
    # Carve up the term data into training and testing
    num_items = int(len(uc_search_terms) * train)
    train_terms = uc_search_terms[:num_items]
    test_terms = uc_search_terms[num_items:]
    
    # Create the training data output
    output1 = ""
    output2 = ""
    for term in train_terms:
        for header in nlu_terms:
            text = "    - " + header + " [" + term + "](query)"
            output1 = output1 + "\n" + text
        output2 = output2 + "\n" + "    - " + " [" + term + "](query)"
    
    # Open a text file to write the data to
    with open('nlu_search.txt', 'w') as txt_file:
        txt_file.write(output1)
        
    # Open a text file to write the data to
    with open('nlu_search_inform.txt', 'w') as txt_file:
        txt_file.write(output2)
        
    # Create test data output
    output3 = ""
    i = 0
    for term in test_terms:
        for header in nlu_terms:
            query = header + " [" + term + "]{\"entity\": \"query\"}"
            text = "- story: search test story " + str(i)
            text = text + "\n" + "  steps:"
            text = text + "\n" + "  - user: |"
            text = text + "\n" + "      " + query
            text = text + "\n" + "    intent: search"
            text = text + "\n" + "  - action: action_perform_search"
            text = text + "\n" + "  - action: action_reset_search_slot"
            text = text + "\n"
            
            output3 = output3 + "\n" + text
            
            i = i + 1
        
        query = "[" + term + "]{\"entity\": \"query\"}"
        text = "- story: search inform test story " + str(i)
        text = text + "\n" + "  steps:"
        text = text + "\n" + "  - user: |"
        text = text + "\n" + "      " + header
        text = text + "\n" + "    intent: search"
        text = text + "\n" + "  - action: utter_search_ask"
        text = text + "\n" + "  - user: |"
        text = text + "\n" + "      " + query
        text = text + "\n" + "  - intent: search_inform"
        text = text + "\n" + "  - action: action_perform_search"
        text = text + "\n" + "  - action: action_reset_search_slot"
        text = text + "\n"
        
        output3 = output3 + "\n" + text
        
    # Open a text file to write the data to
    with open('test_stories.txt', 'w') as txt_file:
        txt_file.write(output3)
        
    return uc_search_terms
            
# Define the command line arguments
parser = argparse.ArgumentParser(description='Text corpus split into sentences')
parser.add_argument('input', help='a text file, PDF or a URL')

# Parse the command-line arguments
args = parser.parse_args()

# Initialize an empty string to store the text
text = ""

# Check if the input is a file, PDF or a URL
if args.input.startswith('http'):
    # Read the text from the URL
    response = requests.get(args.input)
    html = response.text
    
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract the text content
    text = soup.get_text()
elif args.input.endswith('pdf'):
    # Read the text from a PDF
    # Open the PDF file
    with open(args.input, 'rb') as f:
        # Create a PDF object
        pdf = PyPDF2.PdfReader(f)
        
        # Get the number of pages
        num_pages = len(pdf.pages)
        
        # Iterate through each page
        for i in range(num_pages):
            # Extract the text from the page
            page = pdf.pages[i]
            text += page.extract_text()
else:
    # Read the text from the file
    with open(args.input, 'r') as f:
        text = f.read()
        
# Split the text into sentences cleaning the text first
c_text = clean_text(text)

# Tokenize the text
sentences = nltk.sent_tokenize(c_text)
if debug: print(sentences)
if debug: print("================================================")

# Filter out sentences that don't meet criteria
f_sentences = filter_sentences(sentences)
if debug: print(f_sentences)
if debug: print("================================================")

# Clean the specific sentences
c_sentences = clean_sentences(f_sentences)
if debug: print(c_sentences)
if debug: print("================================================")

### Done with Clean Text in Sentence Format

# Step 1: Create list of data to use for NLU and test from the input data
output = create_NLU(c_sentences)
if debug: print(output)
if debug: print("================================================")