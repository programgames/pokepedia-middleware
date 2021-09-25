from api.wikimedia import wikimedia_session

class Auth:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def get_login_token(self, endpoint: str):
        params = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }
        result = wikimedia_session.get(endpoint, params=params)

        json = result.json()

        return json['query']['tokens']['logintoken']

    def login_request(self, logintoken: str, endpoint: str):
        params = {
            "action": "login",
            "lgname": self.user,
            "lgpassword": self.password,
            "lgtoken": logintoken,
            "format": "json"
        }
        result = wikimedia_session.post(endpoint, data=params)

    def get_crsf_token(self, endpoint: str):
        params = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        result = wikimedia_session.get(endpoint, params=params)

        json = result.json()

        token = json['query']['tokens']['csrftoken']
        return token
