FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade

RUN mkdir -p /incameo/django-api/app

WORKDIR /incameo/django-api

COPY api-service/requirements.txt requirements.txt

COPY api-service/app app/.

RUN pip install -r requirements.txt
