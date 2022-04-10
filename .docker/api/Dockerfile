FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade

WORKDIR /incameo/django-api/app

COPY api-service/requirements.txt ../requirements.txt

COPY api-service/app .

COPY .docker/api/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

RUN pip install -r ../requirements.txt

ENTRYPOINT ["entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]