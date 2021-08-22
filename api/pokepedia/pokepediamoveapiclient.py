from api import Auth
from api.pokepedia.client import PokepediaClient
from util.helper import move_set_helper


class PokepediaMoveApiClient(PokepediaClient):
    def __init__(self, client: PokepediaClient, auth: Auth):
        super().__init__(auth)
        self.client = client

    def get_pokemon_moves(self, name: str, generation: int, move_type: str, version_group_name=None, dt=None) -> list:
        if (move_type == move_set_helper.TUTOR_TYPE or move_type == move_set_helper.MACHINE_TYPE) \
                and not version_group_name:
            raise RuntimeError('argument $versionGroupName is required for %s type'.format(move_type))

        sections = self.get_move_sections(name, generation)
        section = self.get_section_index_by_pokemon_move_type_and_generation(move_type, sections, generation,
                                                                             version_group_name, dt)

    def get_move_sections(self, name: str, generation: int):
        if generation < 7:
            sections_url = 'https://www.pokepedia.fr/api.php?action=parse&format=json&page={}/G%C3%A9n%C3%A9ration_{}&prop=sections&errorformat=wikitext&disabletoc=1' \
                .format(name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'), generation)
        else:
            sections_url = 'https://www.pokepedia.fr/api.php?action=parse&format=json&page={}&prop=sections&errorformat=wikitext' \
                .format(name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'))

        return self.client.format_section_by_url(sections_url)

    def get_section_index_by_pokemon_move_type_and_generation(self, move_type: str, sections: list, generation: int,
                                                              version_group_name: str,
                                                              dt: bool):
        if generation < 7:

