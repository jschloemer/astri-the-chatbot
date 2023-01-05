# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:3.4.0

# Change back to root user to install dependencies
USER root

#Use subdirectory as working directory
WORKDIR /app
#COPY requirements.txt ./
#COPY ./actions /app/actions
#COPY ./index /app/index

# To install system dependencies
#RUN apt-get update -qq && \
##    apt-get install -y <NAME_OF_REQUIRED_PACKAGE> && \
##    apt-get clean && \
##    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# To install packages from PyPI
RUN /opt/venv/bin/python -m pip install --no-cache-dir --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pandas openai elasticsearch PyYAML

# Switch back to non-root to run code
USER 1001