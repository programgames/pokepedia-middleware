from middleware.api.wikimedia.auth import Auth
from middleware.api.wikimedia.client import WikimediaClient


class PokepediaClient(WikimediaClient):
    """ Basic class to make basic request to pokepedia
    """
    ENDPOINT = "https://www.pokepedia.fr/api.php"

    token = None

    def __init__(self, auth: Auth):
        self.auth = auth

    def login(self):
        login_token = self.auth.get_login_token(self.ENDPOINT)
        self.auth.login_request(login_token, self.ENDPOINT)
        self.token = self.auth.get_crsf_token(self.ENDPOINT)

    def upload(self, section: int, page: str, wikitext: str, summary: str):
        parameters = {
            'action': 'edit',
            'section': section,
            'title': page.replace('%27', '\''),
            'text': wikitext,
            'format': 'json',
            'bot': True,
            'nocreate': True,
            'token': self.token,
            'summary': summary
        }
        WikimediaClient.edit(self, self.ENDPOINT, parameters)
