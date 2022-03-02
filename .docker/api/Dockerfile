FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade

RUN mkdir -p /incameo/django-api

WORKDIR /incameo/django-api

COPY api-service/requirements.txt requirements.txt

COPY api-service/app .

RUN pip install -r requirements.txt
