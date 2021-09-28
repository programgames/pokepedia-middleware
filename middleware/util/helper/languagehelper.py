from pokedex.db.tables import Language

from middleware.connection.conn import session
from pokedex.db.util import get as getobject

french = getobject(session, Language, u'fr')  # type: Language
