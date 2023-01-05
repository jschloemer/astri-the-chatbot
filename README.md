# astri-the-chatbot
Astri is a chatbot specifically for satellite applications. Astro is powered by Rasa and will continue to add features over time.

## Installation
Astri uses the index folder to hold the necessary data structures it uses to search and provide information back to the user. The specific files it needs are:
- acronyms.json {Key value pair - acronym :: Acronym Meeting}
- parts.json {Key value part - part/subsystem :: Description}
- ... search files ...

Spacy requires a small package to be downloaded using the command.

    python3 -m spacy download en_core_web_sm

## OpenAI Instructions

The user must have an openAI account to use the openAI features. Specifically, the API key needs to be generated from the website and stored in the actionConfig.yml file

## Running the server

    rasa run -m models --enable-api --cors "*"
    rasa run actions

## Docker Setup

# Extend the Rasa SDK Image

    docker build . -t rasa/rasa-sdk:3.4.0

# Create the docker network

    docker network create elastic

# Start the network

    docker run --name es-node01 --net elastic -p 9200:9200 -p 9300:9300 -t docker.elastic.co/elasticsearch/elasticsearch:8.5.3
    docker run --name kib-01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.5.3
    docker run -v $(pwd):/app --name astri-nlu -p 5005:5005 --net elastic rasa/rasa:3.4.0-full run -m models --enable-api --cors "*"
    docker run --name astri-act -p 5055:5055 -v $(pwd)/actions:/app/actions -v $(pwd)/index:/app/index --net elastic rasa/rasa-sdk:3.4.0