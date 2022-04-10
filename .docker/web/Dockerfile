FROM node:17.6-alpine

RUN apk update && apk upgrade

WORKDIR /incameo/nuxt-web/app

COPY web-service/app .

RUN npm install
