# Download base image ubuntu 20.04
FROM ubuntu:20.04

# Disactivate the interactive dialogue
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository and install Python, pip & git from Ubuntu software repository
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3.8 python3-distutils && \
    apt-get install -y sudo curl make && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.8 get-pip.py && \
    rm get-pip.py && \
    apt-get install -y git

# Configure git account
RUN git config --global user.name "ywsyws" && \
    git config --global user.email "channing.platevoet@gmail.com" && \
    git config --global credential.helper store

# OPTIONAL: to configuer input language
# First argument is the name of the environment variable, e.g., LANG, LC_ALL
# Seconde argument is the value of the environment variable, e.g., C.UTF-8
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Create a work directory
RUN mkdir /app

# Set work directory
WORKDIR /app

# Copy the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Install al the required libraries (REPLACED BY THE LINE ABOVE IF USING VIRTUAL ENVIRONMENT)
RUN pip install -r requirements.txt

# Copy the local working directory to docker
# Can omit for the development stage. But usually just keep it.
# Crucial in production to copy the snapshots of our code to the image.
COPY . .

# Set FLASK_APP to app.py
ENV FLASK_APP=app.py FLASK_DEBUG=1

# Define the port
EXPOSE 5000

# Set the default command
CMD flask run --host=0.0.0.0 --port=5000