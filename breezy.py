import requests
import yaml
import json
from time import sleep


class BreezyError(Exception):
    pass


class BreezyAPI:
    API_URL = "https://api.breezy.hr/v3/"

    def __init__(self):
        with open('auth.yaml', 'r') as file:
            config = yaml.safe_load(file)
        self.email = config['email']
        self.password = config['password']
        self.token = self._get_token()

    def call(self, endpoint: str, method: str = 'GET', params: dict = None,
             data: dict = None) -> dict:
        assert method in ['GET', 'POST', 'PUT'], 'Wrong method provided'
        while True:
            # jsonify data if using POST/PUT methods
            if method != 'GET':
                data = json.dumps(data)

            response = requests.request(
                method,
                self.API_URL + endpoint,
                headers={
                    "Authorization": self.token,
                    "Accept": "*/*",
                    "accept-encoding": "gzip, deflate",
                    "content-type": "application/json"
                },
                params=params,
                data=data
            )
            if response.status_code == 401:
                print('Status code 401, getting new token')
                self.token = self._get_token()
            elif response.status_code == 429:
                print('Exceeded API rate limit, sleeping 10 seconds')
                sleep(10)
            elif response.status_code == 200:
                return response.json()
            elif response.status_code == 204:
                return None
            elif response.status_code == 500:
                raise BreezyError(response.json()['error'])
            elif response.status_code == 504:
                print('504 error, sleeping 30 seconds')
                sleep(30)
            else:
                raise Exception(f'response code: {response.status_code}\n'
                                f'response text: {response.text}')

    def _get_token(self) -> str:
        token = requests.post(
            self.API_URL + "signin",
            data={"email": self.email, "password": self.password}
        )
        if token.status_code != 200:
            raise BreezyError('Error obtaining token\nError '
                              f'{token.status_code} > '
                              f'{token.json()}')
        return token.json()['access_token']
