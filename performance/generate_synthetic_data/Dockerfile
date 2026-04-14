FROM python:3.12 AS base

WORKDIR /code

RUN apt-get update && apt-get install -y jq

# Copy requirements.txt and install the packages early during the build
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src ./src
COPY generate_synthetic_data.py .
