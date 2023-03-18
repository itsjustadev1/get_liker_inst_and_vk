import requests
import json
from headers import headersChrome

session = requests.Session()

headers = headersChrome


def getLikers(id):
    result = []
    res = session.get(
        f'https://www.instagram.com/api/v1/media/{id}/likers/', headers=headersChrome)
    res = json.loads(res.text)
    users = res['users']
    for el in users:
        result.append(el['username'])
    return result
