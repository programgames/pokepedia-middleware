from pokedex.db.multilang import MultilangSession
from pokedex.db import connect
import os
from util.helper.kernelhelper import get_project_root
from dotenv import load_dotenv

load_dotenv()
connString = 'sqlite:///' + get_project_root() + os.sep + os.getenv('DATABASE_PATH')
session = connect(connString)  # type: MultilangSession
