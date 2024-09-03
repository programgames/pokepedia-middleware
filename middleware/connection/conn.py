from middleware.util.helper import filesystemhelper
from pokeapi.db.multilang import MultilangSession
from pokeapi.db import connect
import os
from dotenv import load_dotenv

load_dotenv()
connString = 'sqlite:///' + os.path.join(filesystemhelper.ROOT_DIR, os.getenv('DATABASE_PATH'))
session = connect(connString)  # type: MultilangSession
