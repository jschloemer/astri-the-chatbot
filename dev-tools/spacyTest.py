# Designed to be a test for spacy tasks. 
# Author: Jeff Schloemer
# Date: 01/24/2023

import nltk

# Tokenize the sentence
sentence = "The SP500 is a the initialization procedure for a satellite."
tokens = nltk.word_tokenize(sentence)

# Tag the tokens with their part of speech
tagged_tokens = nltk.pos_tag(tokens)

# Iterate over the tagged tokens
for i, (token, tag) in enumerate(tagged_tokens):
    # Check if the token is a noun
    if tag.startswith('NN'):
        # Check if the next token is a verb
        if (i+1 < len(tagged_tokens) and tagged_tokens[i+1][1].startswith('VB')):
            print("This sentence provides a definition of the noun:", token)
            break
        else:
            print("This sentence does not provide a definition of a noun.")


