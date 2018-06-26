# -*- coding:utf-8 -*-
import requests
import time


def downloadImg(img_url, img_path):
    response = requests.get(img_url)
    img = response.content
    img_path = img_path + '/' + str(time.time()) + '.jpg'
    with open(img_path, 'wb') as f:
        f.write(img)

    return img_path
