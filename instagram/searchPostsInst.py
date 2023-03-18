import requests
import requests
import json
from headers import headersChrome
from getHeaders import gettingHeaders
hashtagInst = 'тыващекрутой'

session = requests.Session()

headers = headersChrome


def searchPosts(hashtag):
    res = session.get(
        f'https://www.instagram.com/api/v1/tags/web_info/?tag_name={hashtag}', headers=headersChrome)
    try:
        res = json.loads(res.text)
    except Exception:
        gettingHeaders(hashtag)
        res = session.get(
            f'https://www.instagram.com/api/v1/tags/web_info/?tag_name={hashtag}', headers=headersChrome)
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
    while object.get('more_available'):
        offset = res['data']['recent']['next_max_id']
        res = session.get(
            f'https://www.instagram.com/api/v1/tags/web_info/?tag_name={hashtag}&max_id={offset}', headers=headers)
        res = json.loads(res.text)
        for el in res['data']['recent']['sections']:
            for e in el['layout_content']['medias']:
                id = e['media']['pk']
                link = 'https://www.instagram.com/p/' + e['media']['code']
                result.append([id, link])
        object = res['data']['recent']
    return result
