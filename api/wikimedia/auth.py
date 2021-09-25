import requests, pickle


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
        session = requests.session()

        request = requests.get(endpoint, params=params)

        with open('cookies.txt', 'wb') as f:
            pickle.dump(session.cookies, f)

        json = request.json()

        return json['query']['tokens']['logintoken']

    def login_request(self, logintoken: str, endpoint: str):
        params = {
            "action": "login",
            "lgname": self.user,
            "lgpassword": self.password,
            "lgtoken": logintoken,
            "format": "json"
        }

        session = requests.session()

        requests.post(endpoint, data=params)

        with open('cookies.txt', 'wb') as f:
            pickle.dump(session.cookies, f)

    def get_crsf_token(self, endpoint: str):
        params = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        session = requests.session()

        request = requests.get(endpoint, params=params)

        with open('cookies.txt', 'wb') as f:
            pickle.dump(session.cookies, f)

        json = request.json()

        return json['query']['tokens']['csrftoken']
