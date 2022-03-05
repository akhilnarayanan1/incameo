docker build . -f .docker/api/Dockerfile -t incameo-api:dev

docker build . -f .docker/web/Dockerfile -t incameo-web:dev

docker-compose up