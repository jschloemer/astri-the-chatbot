# Created to perform basic web-crawler indexing for the purposes of using for future indexing
# Author: Jeff Schloemer
# Date: 12/28/2022

# First, we need to install the requests, BeautifulSoup, and csv libraries:
# !pip install requests beautifulsoup4 csv argparse

# Import the necessary modules:
import csv
import argparse
import requests
import time
from bs4 import BeautifulSoup

# Use the argparse library to parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('domain', help='The domain to crawl - Example: example.com')
parser.add_argument('start_url', help='The starting URL - Example: http://example.com')
args = parser.parse_args()

# Set the domain and starting URL from the command line arguments
domain = args.domain
start_url = args.start_url

# Initialize a set to store the URLs we have already visited
visited_urls = set()

# Initialize a queue to store the URLs we need to visit
queue = [start_url]

# Set a maximum number of pages to crawl (to avoid getting stuck in an infinite loop)
max_pages = 250

# Set a user agent to use in the HTTP headers (to identify the crawler to the server)
user_agent = 'MyWebCrawler/1.0'

# Open a CSV file to write the data to
with open('urls.csv', 'w', newline='') as csv_file:
    # Create a CSV writer
    writer = csv.writer(csv_file)

    # Start the crawl
    while queue and len(visited_urls) < max_pages:
        # Get the next URL from the queue
        url = queue.pop(0)

        # Send a GET request to the server
        response = requests.get(url, headers={'User-Agent': user_agent})

        # Check the response status code (200 means the request was successful)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the links on the page
            links = soup.find_all('a')

            # Iterate over the links
            for link in links:
                # Get the URL of the link
                link_url = link.get('href')

                # Check if the link is on the same domain and has not been visited yet
                if link_url and domain in link_url and link_url not in visited_urls:
                    # Add the URL to the queue and the visited URLs set
                    queue.append(link_url)
                    visited_urls.add(link_url)

        # Sleep for a short time to avoid overwhelming the server
        time.sleep(1)

    # Write the visited URLs to the CSV file
    for url in visited_urls:
        writer.writerow([url])
