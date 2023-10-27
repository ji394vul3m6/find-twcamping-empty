FROM python:3-slim-buster

RUN mkdir /app
WORKDIR /app
ADD main.py requirement.txt run.sh /app/
RUN pip install -r requirement.txt