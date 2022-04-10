FROM node:17.6-alpine

WORKDIR /incameo/nuxt-web/app

COPY ./web-service/app .

COPY .docker/web/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

RUN npm install

ENTRYPOINT ["entrypoint.sh"]