import requests

class Llama:
    def __init__(self):
        pass

    def getTvl(self, protocol):
        url = f'https://api.llama.fi/protocol/{protocol}'
        headers = {
            'accept': '*/*'
        }

        response = requests.get(url, headers=headers)
        return response
    
    def getAllProtocols(self):
        url = f'https://api.llama.fi/protocols'
        headers = {
            'accept': '*/*'
        }

        response = requests.get(url, headers=headers)
        return response
