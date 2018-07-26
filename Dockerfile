FROM python:3.6-slim

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
