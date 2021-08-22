from api import Auth
from api.wikimedia import Client


class PokepediaClient(Client):

    ENDPOINT = "https://www.pokepedia.fr/api.php"

    def __init__(self,auth: Auth):
        self.auth = auth

    def login(self):
        login_token = self.auth.get_login_token(self.ENDPOINT)
        self.auth.login_request(login_token,self.ENDPOINT)
        return self.auth.get_crsf_token(self.ENDPOINT)