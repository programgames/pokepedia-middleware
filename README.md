- git clone git@github.com:programgames/pokepedia-middleware.git
- cd pokepedia-middleware
- cd pokedex 
- sudo python setup.py develop
- pip install -e pokedex
- cd ..
- pokedex load
- pokedex load -e sqlite:///db.sqlite
