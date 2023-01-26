# Designed to be a standalone processor of project text. The goals as follows:
# - 1) Generate training data and test data to use for Rasa NLU from the core text
# - 2) Identify sentences with acroynms in them
# - 3) Attempt to create meaningful data relationships for easy lookup for Astri
# Author: Jeff Schloemer
# Date: 01/23/2023

# pip install nltk requests PyPDF2 bs4

import nltk
import argparse
import requests
import PyPDF2
import re
import random
import string
from bs4 import BeautifulSoup

# Debug settings
debug = False

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
    c_text = re.sub(r"[^\s\w!@#$5\^&*();:,./?\\<>{}\[\]\-\+=_`~\’\'\"]", ".", i_text)
    return c_text

# Function for parsing through clean sentences for NLU data
def create_NLU(sentences):
    # Create empty lists
    search_terms = []
    max_NLU = 1000
    
    # Go through one sentence at a time
    for sentence in sentences:
        words = sentence.split()
        tot = len(words)
        while (tot > 0):
            pops = 0
            
            # Randomize how many words to bite off
            rand = random.randint(0, 99)
            if rand in range(0,40):
                pops = 2
            elif rand in range(40,70):
                pops = 3
            elif rand in range(70,85):
                pops = 4
            elif rand in range(85,95):
                pops = 5
            else:
                pops = 6
                
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
        
        # Strip of stop words from the start and stop of the phrase (creates an empty list of all stop words)
        tokens = nltk.word_tokenize(c_term)
        while len(tokens) > 0 and tokens[0] in stop_words:
            tokens.pop(0)
        while len(tokens) > 0 and tokens[-1] in stop_words:
            tokens.pop(-1)
            
        # Merge remaining tokens together
        if len(tokens) > 0:
            r_term = ""
            for word in tokens:
                r_term = r_term + " " + word
            c_search_terms.append(r_term.strip())
    
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
    
    # Select the first set for one output and the last set for the other
    first_setup = []
    last_setup = []
    if len(train_terms) > max_NLU:
        first_setup = train_terms[:max_NLU]
        last_setup = train_terms[-max_NLU:]
    else:
        first_setup = train_terms
        last_setup = train_terms
    
    for term in first_setup:
        rand = random.randint(0,2)
        text = "    - " + nlu_terms[rand] + " [" + term.strip() + "](query)"
        output1 = output1 + "\n" + text
    for term in last_setup:
        output2 = output2 + "\n" + "    - " + "[" + term.strip() + "](query)"
    
    # Open a text file to write the data to
    with open('nlu_search.txt', 'w') as txt_file:
        txt_file.write(output1)
        
    # Open a text file to write the data to
    with open('nlu_search_inform.txt', 'w') as txt_file:
        txt_file.write(output2)
        
    # Create test data output
    output3 = ""
    first_setup = []
    max_Test = int(max_NLU * .1)
    if len(test_terms) > max_Test:
        first_setup = test_terms[:max_Test]
    else:
        first_setup = test_terms
    i = 0
    for term in first_setup:
        rand = random.randint(0,2)
        query = nlu_terms[rand] + " [" + term + "]{\"entity\": \"query\"}"
        text = "- story: search test story " + str(i)
        text = text + "\n" + "  steps:"
        text = text + "\n" + "  - user: |"
        text = text + "\n" + "      " + query
        text = text + "\n" + "    intent: search"
        text = text + "\n" + "  - action: action_perform_search"
        text = text + "\n" + "  - action: action_reset_search_slot"
        text = text + "\n"
        
        output3 = output3 + "\n" + text
        
        rand = random.randint(0,2)
        query = "[" + term + "]{\"entity\": \"query\"}"
        text = "- story: search inform test story " + str(i)
        text = text + "\n" + "  steps:"
        text = text + "\n" + "  - user: |"
        text = text + "\n" + "      " + nlu_terms[rand]
        text = text + "\n" + "    intent: search"
        text = text + "\n" + "  - action: utter_search_ask"
        text = text + "\n" + "  - user: |"
        text = text + "\n" + "      " + query
        text = text + "\n" + "  - intent: search_inform"
        text = text + "\n" + "  - action: action_perform_search"
        text = text + "\n" + "  - action: action_reset_search_slot"
        text = text + "\n"
        
        output3 = output3 + "\n" + text
        i = i + 1
        
    # Open a text file to write the data to
    with open('test_stories.txt', 'w') as txt_file:
        txt_file.write(output3)
        
    return uc_search_terms

def check_acro(sentences):
    # Create empty lists
    acronyms = []
    acronym_only_sentences = []
    acronym_expl_sentences = []
    non_acronym_sentences = []
    kvp = []
    
    # Go through one sentence at a time
    for sentence in sentences:
        poss_acro = []
        good_sentence = False
        
        # Look for all-caps words by word
        words = sentence.split()
        for word in words:
            # Strip punctuations
            c_word = word
            for punct in string.punctuation:
                c_word = c_word.strip(punct)
            
            # Look for acronyms words. Must be all caps and at least 2 letters long but can contain dashes
            if re.search(r'^[A-Z][A-Z\-]+$', c_word):
                poss_acro.append(c_word)
        
        # Check to see if the sentence likely makes sense
        # Check to see if it has any stop words
        u_words = set(sentence.split())
        if len(u_words.intersection(stop_words)) > 1:
            good_sentence = True
            
        if good_sentence and len(poss_acro) > 0:
            poss = False
            
            # Check to see if the acronym may be explained in the sentence
            
            # Grab the first letter in a sentence and merge it in
            first_letters = [word[0] for word in words]
            sentword = "".join(first_letters).upper()
            
            for opt in poss_acro:
                acronyms.append(opt)
                
                # Remove the dash option
                simp_acro = re.sub(r"[^\w]", "", opt)
                
                index = sentword.find(simp_acro)
                
                # Check to see if the acronym is in the string of the first letters
                if index != -1:
                    expl = ""
                    for i in range(index,index + len(simp_acro)):
                        expl = expl + " " + words[i]
                    
                    # Check for recursion (acronym in the explaination)
                    index2 = expl.find(opt)
                    if index2 == -1:
                        pair = opt + " ::" + expl
                        kvp.append(pair)
                        poss = True
            if poss:
                acronym_expl_sentences.append(sentence)
            else:
                acronym_only_sentences.append(sentence)
        elif good_sentence:
            non_acronym_sentences.append(sentence)
            
    # Ouput the results...
    u_acronyms = list(set(acronyms))
    printlist = [str(i) for i in u_acronyms]
    printlist.sort()
    printitem = "\n".join(printlist)
    with open("acronyms.txt", "w") as file:
        file.write(printitem)
        
    printlist = [str(i) for i in acronym_only_sentences]
    printitem = "\n".join(printlist)
    with open("acronym_only_sentences.txt", "w") as file:
        file.write(printitem)
    
    printlist = [str(i) for i in acronym_expl_sentences]
    printitem = "\n".join(printlist)
    with open("acronym_expl_sentences.txt", "w") as file:
        file.write(printitem)
        
    printlist = [str(i) for i in non_acronym_sentences]
    printitem = "\n".join(printlist)
    with open("non_acronym_sentences.txt", "w") as file:
        file.write(printitem)
        
    printlist = [str(i) for i in kvp]
    printlist.sort()
    printitem = "\n".join(printlist)
    with open("kvp.txt", "w") as file:
        file.write(printitem)
            
    return [acronym_only_sentences, acronym_expl_sentences, non_acronym_sentences]

def is_def_sentence(sentence):
    # Processing the sentence
    tokens = nltk.word_tokenize(sentence)

    # Tag the tokens with their part of speech
    tagged_tokens = nltk.pos_tag(tokens)

    # Iterate over the tagged tokens
    for i, (token, tag) in enumerate(tagged_tokens):
        # Check if the token is a noun
        if tag.startswith('NN'):
            # Check if the next token is a verb
            if (i+1 < len(tagged_tokens) and tagged_tokens[i+1][1].startswith('VB')):
                return True
            else:
                return False

def find_relations(sentences):
    relations = []
    
    for sentence in sentences:
        if is_def_sentence(sentence):
            relations.append(sentence)
            
    printitem = "\n".join(relations)
    with open("relations.txt", "w") as file:
        file.write(printitem)
            
    return relations
    
            
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
print("Parsed and Created " + str(len(output)) + " Unique NLU Expressions")

# Step 2: Parse sentences for Acronyms
[output1, output2, output3] = check_acro(c_sentences)
if debug: print(output2)
if debug: print("================================================")
print("Parsed and Created " + str(len(output1) + len(output2) + len(output3)) + " Unique Acronym Sentences")

# Step 3: Create meaningful relationships
output4 = find_relations(c_sentences)
if debug: print(output4)
if debug: print("================================================")
print("Parsed and Created " + str(len(output4)) + " Sentence Relations")