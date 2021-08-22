from api import Auth
from api.pokepedia.client import PokepediaClient
from exception import NotAvailableError
from util.helper import move_set_helper
import re


class PokepediaMoveApiClient(PokepediaClient):
    def __init__(self, client: PokepediaClient, auth: Auth):
        super().__init__(auth)
        self.client = client

    def get_pokemon_moves(self, name: str, generation: int, move_type: str, version_group_name=None, dt=None) -> dict:
        if (move_type == move_set_helper.TUTOR_TYPE or move_type == move_set_helper.MACHINE_TYPE) \
                and not version_group_name:
            raise RuntimeError('argument version_group_name is required for %s type'.format(move_type))

        sections = self.get_move_sections(name, generation)
        section = self.get_section_index_by_pokemon_move_type_and_generation(move_type, sections, generation,
                                                                             version_group_name, dt)
        if generation < 7:
            page = '{}/Génération_{}'.format(generation,
                                             name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'))
            url = 'https://www.pokepedia.fr/api.php?action=parse&format=json&page={}&prop=wikitext&errorformat=wikitext&section={}&disabletoc=1' \
                .format(page, section)
        else:
            page = name.replace('’', '%27')
            url = 'https://www.pokepedia.fr/api.php?action=parse&format=json&page={}&prop=wikitext&errorformat=wikitext&section={}&disabletoc=1' \
                .format(page, section)
        content = self.client.parse(url)
        wikitext = content['parse']['wikitext'][0]  # TODO test getting first element in this list
        wikitext = re.split(r'/\R?^/m', wikitext)

        return {
            wikitext: wikitext,
            section: section,
            page: page,

        }

    def get_move_sections(self, name: str, generation: int)-> dict:
        if generation < 7:
            sections_url = 'https://www.pokepedia.fr/api.php?action=parse&format=json&page={}/G%C3%A9n%C3%A9ration_{}&prop=sections&errorformat=wikitext&disabletoc=1' \
                .format(name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'), generation)
        else:
            sections_url = 'https://www.pokepedia.fr/api.php?action=parse&format=json&page={}&prop=sections&errorformat=wikitext' \
                .format(name.replace('’', '%27').replace('\'', '%27').replace(' ', '_'))

        return self.client.format_section_by_url(sections_url)

    def get_section_index_by_pokemon_move_type_and_generation(self, move_type: str, sections: dict, generation: int,
                                                              version_group_name: str,
                                                              dt: bool)-> int:


        if move_type == move_set_helper.LEVELING_UP_TYPE and generation <= 6:
            return sections['Capacités apprises//Par montée en niveau']
        elif move_type == move_set_helper.LEVELING_UP_TYPE and generation == 7:
            return sections['Capacités apprises//Par montée en niveau//Septième génération']
        elif move_type == move_set_helper.LEVELING_UP_TYPE and generation == 8:
            return sections['Capacités apprises//Par montée en niveau//Huitième génération']
        elif move_type == move_set_helper.MACHINE_TYPE and generation <= 6:
            return sections['Capacités apprises//Par CT/CS']
        elif move_type == move_set_helper.MACHINE_TYPE and generation == 7 and version_group_name != "Pokémon : Let's Go, Pikachu et Let's Go, Évoli":
            return sections['Capacités apprises//Par CT/CS//Septième génération//Pokémon Soleil et Lune et Pokémon Ultra-Soleil et Ultra-Lune']
        elif move_type == move_set_helper.MACHINE_TYPE and generation == 7 and version_group_name == "Pokémon : Let's Go, Pikachu et Let's Go, Évoli":
            return sections["Capacités apprises//Par CT/CS//Septième génération//Pokémon : Let's Go, Pikachu et Let's Go, Évoli"]
        elif move_type == move_set_helper.MACHINE_TYPE and generation == 8 and not dt:
            return sections["Capacités apprises//Par CT/CS//Huitième génération"]
        elif move_type == move_set_helper.MACHINE_TYPE and generation == 8 and dt:
            return sections["Capacités apprises//Par DT//Huitième génération"]
        elif move_type == move_set_helper.EGG_TYPE and generation == 1:
            raise NotAvailableError("egg mooves are not available in gen 1")
        elif move_type == move_set_helper.EGG_TYPE and 2 <= generation <= 6:
            return sections["Capacités apprises//Par reproduction"]
        elif move_type == move_set_helper.EGG_TYPE and generation == 7:
            return sections["Capacités apprises//Par reproduction//Septième génération"]
        elif move_type == move_set_helper.EGG_TYPE and generation == 8:
            return sections["Capacités apprises//Par reproduction//Huitième génération"]
        elif move_type == move_set_helper.TUTOR_TYPE and generation == 1:
            raise NotAvailableError("tutor mooves are not available in gen 1")
        elif move_type == move_set_helper.TUTOR_TYPE and generation == 2 and version_group_name != 'Pokémon Cristal':
            raise NotAvailableError("tutor mooves are only available in crystal version for gen 2")
        elif move_type == move_set_helper.TUTOR_TYPE and generation == 2 and version_group_name == 'Pokémon Cristal':
            return sections["Capacités apprises//Par Donneur de capacités//Pokémon Cristal"]
        elif move_type == move_set_helper.TUTOR_TYPE and generation == 3 and version_group_name == 'Pokémon Rubis et Saphir':
            raise NotAvailableError("tutor mooves are not available in ruby/sapphir")
        elif move_type == move_set_helper.TUTOR_TYPE and 3 <= generation <= 6:
            return sections["Capacités apprises//Par Donneur de capacités//{}".format(version_group_name)]
        elif move_type == move_set_helper.TUTOR_TYPE and generation == 7:
            return sections["Capacités apprises//Par Donneur de capacités//Septième génération"]
        elif move_type == move_set_helper.TUTOR_TYPE and generation == 8:
            return sections["Capacités apprises//Par Donneur de capacités//Huitième génération"]

