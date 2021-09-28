from middleware.util.helper import filesystemhelper
from pokedex.db.multilang import MultilangSession
from pokedex.db import connect
import os
from dotenv import load_dotenv

load_dotenv()
connString = 'sqlite:///' + os.path.join(filesystemhelper.ROOT_DIR, os.getenv('DATABASE_PATH'))
session = connect(connString)  # type: MultilangSession
