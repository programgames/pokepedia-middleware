from middleware.api.wikimedia.auth import Auth
from middleware.api.wikimedia.client import WikimediaClient


class PokepediaClient(WikimediaClient):
    """
    Basic class to make requests to Poképédia's API.
    Handles authentication and editing pages.
    """
    ENDPOINT = "https://www.pokepedia.fr/api.php"

    def __init__(self, auth: Auth):
        self.auth = auth
        self.token = None

    def login(self):
        try:
            login_token = self.auth.get_login_token(self.ENDPOINT)
            self.auth.login_request(login_token, self.ENDPOINT)
            self.token = self.auth.get_crsf_token(self.ENDPOINT)
            if not self.token:
                raise RuntimeError("Failed to retrieve CSRF token.")
        except Exception as e:
            raise RuntimeError(f"Login failed: {e}")

    def upload(self, section: int, page: str, wikitext: str, summary: str):
        if not self.token:
            raise RuntimeError("Upload failed: No valid CSRF token found. Please login first.")

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

        try:
            super().edit(self.ENDPOINT, parameters)
        except Exception as e:
            raise RuntimeError(f"Upload failed: {e}")
