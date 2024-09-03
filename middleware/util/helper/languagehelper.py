from pokeapi.db.tables import Language

from middleware.connection.conn import session
from pokeapi.db.util import get as getobject

french = getobject(session, Language, u'fr')  # type: Language
