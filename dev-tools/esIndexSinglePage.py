# Created as an examples to practice indexing a set of urls using elasticsearch
# Author: Jeff Schloemer
# Date: 12/28/2022

# First, we need to install the elasticsearch and requests libraries:
#!pip install elasticsearch requests

# import the necessary modules:
import elasticsearch
import requests

# Connect to the Elasticsearch cluster
es = elasticsearch.Elasticsearch()

# Define a list of URLs to index
urls = [
    'http://example.com/page1',
    'http://example.com/page2',
    'http://example.com/page3'
]

# Iterate over the URLs, fetching the HTML content and indexing it in Elasticsearch
for url in urls:
    response = requests.get(url)
    html = response.text
    doc = {
        'url': url,
        'html': html
    }
    es.index(index='webpage', doc_type='page', body=doc)
