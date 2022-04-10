FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade

WORKDIR /incameo/django-api/app

COPY api-service/requirements.txt ../requirements.txt

COPY api-service/app .

RUN pip install -r ../requirements.txt
