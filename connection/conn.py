from pokedex.db.multilang import MultilangSession
from pokedex.db import connect
import os
from util.helper.kernelhelper import get_project_root

connString = 'sqlite:///' + get_project_root() + os.sep + 'db.sqlite'
session = connect(connString)  # type: MultilangSession
