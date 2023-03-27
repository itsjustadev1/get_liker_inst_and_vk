import requests
import requests
import json
from . import headers
from instagram.getHeaders import gettingHeaders
import importlib

hashtag = 'тыващекрутой'
session = requests.Session()


def searchPosts(hashtag):
    headers_get = headers.headersChrome
    res = session.get(
        f'https://www.instagram.com/api/v1/tags/web_info/?tag_name={hashtag}', headers=headers_get)
    try:
        res = json.loads(res.text)
    except Exception:
        gettingHeaders(hashtag)
        importlib.reload(headers)
        headers_get = headers.headersChrome
        res = session.get(
            f'https://www.instagram.com/api/v1/tags/web_info/?tag_name={hashtag}', headers=headers_get)
        res = json.loads(res.text)
    result = []
# top posts
    # for el in res['data']['top']['sections']:
    #     for e in el['layout_content']['medias']:
    #         id = e['media']['pk']
    #         link = 'https://www.instagram.com/p/' + e['media']['code']
    #         result.append([id, link])
 # recent posts
    for el in res['data']['recent']['sections']:
        for e in el['layout_content']['medias']:
            id = e['media']['pk']
            link = 'https://www.instagram.com/p/' + e['media']['code']
            result.append([id, link])
    object = res['data']['recent']
# additional recent posts
    headers_get = headers.headersChrome
    while object.get('more_available'):
        offset = res['data']['recent']['next_max_id']
        res = session.get(
            f'https://www.instagram.com/api/v1/tags/web_info/?tag_name={hashtag}&max_id={offset}', headers=headers_get)
        res = json.loads(res.text)
        for el in res['data']['recent']['sections']:
            for e in el['layout_content']['medias']:
                id = e['media']['pk']
                link = 'https://www.instagram.com/p/' + e['media']['code']
                result.append([id, link])
        object = res['data']['recent']
    return result


def try_searchPosts(hashtag):
    headers_get = headers.headersChrome
    res = session.get(
        f'https://www.instagram.com/api/v1/tags/web_info/?tag_name={hashtag}', headers=headers_get)
    try:
        res = json.loads(res.text)
    except:
        return ('error')
