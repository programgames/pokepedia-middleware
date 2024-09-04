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

### Without docker
- make setup
- make serve ( optionnal , it start a server for the API)
- make build-db
- cd ..
- python manage.py migrate ( for app migrations )

### With docker
- make docker-setup
- make docker-build-db
- make hasura-apply

## Middleware starting
- cp .env.dist .env
- setup your env variables
- python middleware.py init
