from pokedex.db.multilang import MultilangSession
from pokedex.db import connect
import os
from .helper import kernel_helper

connString = 'sqlite:///' + kernel_helper.get_project_root() + os.sep + 'db.sqlite'
session = connect(connString)  # type: MultilangSession
