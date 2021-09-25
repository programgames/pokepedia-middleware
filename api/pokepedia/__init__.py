from api.pokepedia.client import PokepediaClient
from api.wikimedia.auth import Auth
from dotenv import load_dotenv
import os

load_dotenv()

pokepedia_client = PokepediaClient(Auth(os.getenv('POKEPEDIA_USER'),os.getenv('POKEPEDIA_PASSWORD'),))
pokepedia_client.login()