from pokeapi.db import util
from middleware.connection.conn import session


def get(table, identifier):
    return util.get(session, table, identifier)
