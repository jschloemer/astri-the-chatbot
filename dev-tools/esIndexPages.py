# Created as an examples to practice indexing a set of urls using elasticsearch
# Author: Jeff Schloemer
# Date: 12/28/2022

# First, we need to install the elasticsearch and requests libraries:
#!pip install elasticsearch requests

# import the necessary modules:
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import csv

# Connect to the Elasticsearch cluster
es = Elasticsearch(hosts=['https://localhost:9200'], http_auth=('elastic', '-gduI5VLflBbyGt4ozD6'), verify_certs=False)

# Check if the 'webpage' index exists
if es.indices.exists(index='webpage'):
    # Delete the 'old-index' index
    es.indices.delete(index='webpage')

# Define a list of URLs to index
# Create an empty list to store the URLs
urls = []

# Open the CSV file
with open('example-data/upSatUrls.csv', 'r') as f:
    # Create a CSV reader
    reader = csv.reader(f)
    
    # Iterate over the rows of the CSV
    for row in reader:
        # Extract the URL from the first column of the row
        url = row[0]
        
        # Add the URL to the list
        urls.append(url)
        
# Iterate over the URLs
id = 1
for url in urls:
    # Retrieve the HTML from the URL
    r = requests.get(url)
    html = r.text
    
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract the text content
    text = soup.get_text()
    
    # Index the text content in Elasticsearch
    es.index(index='webpage', id=id, document={'text': text, 'url': url, 'timestamp': datetime.now()})
    id = id + 1

es.indices.refresh(index="webpage")

