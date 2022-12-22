# Requirements:

-Python 3.8

# Install :

## Middleware setup 
- git clone git@github.com:programgames/pokepedia-middleware.git
- cd pokepedia-middleware
- git submodule init
- git submodule update
- pip install -r requirements.txt

## Pokeapi setup
- cd pokeapi
- make install

[//]: # (### Without docker)

[//]: # (- make setup)

[//]: # (- make serve &#40; optionnal , it start a server for the API&#41;)

[//]: # (- make build-db)

[//]: # (- cd ..)

[//]: # (- python manage.py migrate &#40; for app migrations &#41;)

### With docker
- make docker-setup
- make docker-build-db
- make hasura-apply

## Middleware starting
- cd ..
- make migrate
- python manage.py init
- cp .env.dist .env
- setup your env variables
