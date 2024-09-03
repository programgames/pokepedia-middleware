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
- make setup
- make serve ( optionnal )
- make build-db
- make docker-setup
- make docker-build-db

## Middleware starting
- cp .env.dist .env
- setup your env variables
- python middleware.py init
