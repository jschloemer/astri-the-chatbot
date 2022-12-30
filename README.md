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

The user must have an openAI account to use the openAI features. Specifically, the API key needs to be generated from the website and stored for local use in an environment variable called OPENAI_API_KEY

## Running the server

    rasa run -m models --enable-api --cors "*"
    rasa run actions