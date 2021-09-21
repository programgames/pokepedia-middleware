from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.types import Integer, Unicode, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from pokedex.db.tables import Pokemon, TableBase, VersionGroup, Move, Generation, Language, Type
from sqlalchemy import and_


class MoveNameChangelog(TableBase):
    __tablename__ = 'move_name_changelog'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(79), nullable=False, index=True)
    generation_id = Column(Integer, ForeignKey('generations.id'), nullable=False)
    move_id = Column(Integer, ForeignKey('moves.id'), nullable=False)
    language_id = Column(Integer, ForeignKey('languages.id'), nullable=False)
    generation = relationship(Generation, innerjoin=True, lazy='joined')
    move = relationship(Move, innerjoin=True, lazy='joined')
    language = relationship(Language, innerjoin=True, lazy='joined')


pkm_availability_form_table = Table("pkm_availability_form", TableBase.metadata,
                                    Column("parent_id", Integer, ForeignKey("pokemon_move_availability.id"),
                                           primary_key=True),
                                    Column("child_id", Integer, ForeignKey("pokemon_move_availability.id"),
                                           primary_key=True),
                                    Column("version_group_id", Integer, ForeignKey("version_groups.id"),
                                           primary_key=True)
                                    )


class PokemonMoveAvailability(TableBase):
    __tablename__ = 'pokemon_move_availability'
    id = Column(Integer, primary_key=True, autoincrement=True)
    version_group_id = Column(Integer, ForeignKey('version_groups.id'), nullable=False)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    is_default = Column(Boolean, nullable=False, default=True)
    has_pokepedia_page = Column(Boolean, nullable=False, default=True)
    forms = relationship('PokemonMoveAvailability',
                         secondary=pkm_availability_form_table,
                         primaryjoin=and_(id == pkm_availability_form_table.c.parent_id,
                                          version_group_id == pkm_availability_form_table.c.version_group_id),
                         secondaryjoin=and_(id == pkm_availability_form_table.c.child_id,
                                            version_group_id == pkm_availability_form_table.c.version_group_id),
                         innerjoin=True,
                         backref='childs')

    pokemon = relationship(Pokemon, innerjoin=True, lazy='joined')
    version_group = relationship(VersionGroup, innerjoin=True, lazy='joined')


class PokemonTypePast(TableBase):
    __tablename__ = 'pokemon_type_past'
    id = Column(Integer, primary_key=True, autoincrement=True)
    slot = Column(Integer, nullable=False)
    generation_id = Column(Integer, ForeignKey('generations.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('types.id'), nullable=False)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    generation = relationship(Generation, innerjoin=True, lazy='joined')
    type = relationship(Type, innerjoin=True, lazy='joined')
    pokemon = relationship(Pokemon, innerjoin=True, lazy='joined')

class CacheItem(TableBase):
    __tablename__ = 'cache_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(Text, nullable=False)
    data = Column(JSON, nullable=False)

move_name_changelog_table = MoveNameChangelog()
pokemon_move_availability_table = PokemonMoveAvailability()
pokemon_type_past_table = PokemonTypePast()
cache_item_table = CacheItem()