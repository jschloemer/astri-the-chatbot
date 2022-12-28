# Created to convert a CSV file to JSON for ingest by the chatbot
# Author: Jeff Schloemer
# Date: 12/28/2022

# Runtime instructions - To use this script, you can run it from the command line with the name of the CSV file as an argument. For example: python script.py data.csv

import argparse
import csv
import json

# Use the argparse library to parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('csv_file', help='The CSV file to convert')
args = parser.parse_args()

# Open the CSV file and read in the data
with open(args.csv_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Create an empty list to store the data
    data = []

    # Iterate over the rows of the CSV file, adding each row to the data list as a dictionary
    for row in csv_reader:
        data.append(row)

# Open a new file to write the JSON data to
json_file_name = args.csv_file.replace('.csv', '.json')
with open(json_file_name, 'w') as json_file:
    # Write the data to the JSON file
    json.dump(data, json_file)

print(f'Successfully converted {args.csv_file} to {json_file_name}')

