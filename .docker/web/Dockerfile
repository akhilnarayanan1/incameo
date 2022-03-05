FROM node:17.6-alpine

RUN apk update && apk upgrade

RUN mkdir -p /incameo/vue-web/app

WORKDIR /incameo/vue-web/app

COPY web-service/app .

RUN npm install
