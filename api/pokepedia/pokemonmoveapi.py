from api.pokepedia.pokepediamoveapiclient import PokepediaMoveApiClient


class PokepediaMoveApi:
    def __init__(self,move_client: PokepediaMoveApiClient):
        self.move_client = move_client
    