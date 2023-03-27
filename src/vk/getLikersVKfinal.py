import re
import requests
import math
from config import access_token
from config import hashtagVk
# есть задача искать новости по хэштэгам и получать id людей, лайкнувших запись = done


def getLikersIds(owner, item, access_token):
    a = requests.get(
        f"https://api.vk.com/method/likes.getList?type=post&owner_id={owner}&item_id={item}&v=5.81&access_token={access_token}")
    requestInfo = requests.Response.json(a)
    countOfLikes = requestInfo['response']['count']
    i = 0
    if countOfLikes > 100:
        countOfLikes = (countOfLikes) / 100
        numberOfResultPages = math.floor(countOfLikes)
        i = numberOfResultPages

    arrayOfIds = []

    while i >= 0:
        a = requests.get(
            f"https://api.vk.com/method/likes.getList?type=post&owner_id={owner}&item_id={item}&offset={i*100}&v=5.81&access_token={access_token}")
        listOfIds = requests.Response.json(a)
        arrayOfIds += listOfIds['response']['items']
        i -= 1
    return arrayOfIds


def getPostsByHashtag(hashtagVk, access_token):
    resultingArrayOfPosts = []
    i = 0
    posts = requests.get(
        f'https://api.vk.com/method/newsfeed.search?q=%23{hashtagVk}&v=5.131&access_token={access_token}')
    objectWithPosts = requests.Response.json(posts)
    while i < len(objectWithPosts['response']['items']):
        owner = (objectWithPosts['response']['items'][i]['owner_id'])
        item_id = (objectWithPosts['response']['items'][i]['id'])
        resultingArrayOfPosts.append(f"vk.com/wall{owner}_{item_id}")
        i += 1
    while 'next_from' in objectWithPosts['response']:
        offset = objectWithPosts['response']['next_from']
        posts = requests.get(
            f'https://api.vk.com/method/newsfeed.search?q=%23{hashtagVk}&v=5.131&access_token={access_token}&start_from={offset}')
        objectWithPosts = requests.Response.json(posts)
        j = 0
        while j < len(objectWithPosts['response']['items']):
            owner = (objectWithPosts['response']['items'][j]['owner_id'])
            item_id = (objectWithPosts['response']['items'][j]['id'])
            resultingArrayOfPosts.append(f"vk.com/wall{owner}_{item_id}")
            j += 1
    return resultingArrayOfPosts


def getPostsToLike(likerID):
    postsToLike = []
    arrayOfPosts = getPostsByHashtag(hashtagVk, access_token)
    for element in arrayOfPosts:
        ownerAndItem = re.split("vk.com/wall|_", str(element))
        ownerAndItem.pop(0)

        owner = ownerAndItem[0]
        item = ownerAndItem[1]
        likersArray = getLikersIds(owner, item, access_token)
        if likerID in likersArray:
            continue
        else:
            postsToLike.append(element)
    return postsToLike


def translateToID(shortName, access_token):
    a = requests.get(
        f"https://api.vk.com/method/users.get?&user_ids={shortName}&v=5.81&access_token={access_token}")
    userObject = requests.Response.json(a)
    if len(userObject['response']):
        return (userObject['response'][0]['id'])


def tryGettingPage(name, access_token):
    a = requests.get(
        f"https://api.vk.com/method/users.get?&user_ids={name}&v=5.81&access_token={access_token}")
    userObject = requests.Response.json(a)
    return userObject
