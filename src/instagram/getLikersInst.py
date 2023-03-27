import requests
import json
from . import headers
import importlib

session = requests.Session()


def getLikers(id):
    headers_get = headers.headersChrome
    result = []
    res = session.get(
        f'https://www.instagram.com/api/v1/media/{id}/likers/', headers=headers_get)
    try:
        res = json.loads(res.text)

    except:
        importlib.reload(headers)
        headers_get = headers.headersChrome
        res = session.get(
            f'https://www.instagram.com/api/v1/media/{id}/likers/', headers=headers_get)
        res = json.loads(res.text)

    users = res['users']
    for el in users:
        result.append(el['username'])
    return result
