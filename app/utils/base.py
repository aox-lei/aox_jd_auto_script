# -*- coding:utf-8 -*-
import os
import requests
import json
from requests_html import HTML
from app.utils.web_browser import openWithWebBrowser


class base(object):
    COOKIE_PATH = './data/cookie.txt'
    HOME_URL = 'https://home.jd.com/'
    LOGIN_URL = 'https://passport.jd.com/new/login.aspx'
    INDEX_URL = 'https://www.jd.com/'

    def __init__(self,):
        self.session = requests.Session()
        self.load_cookie()

    def check_login(self):
        ''' 检测登录 '''
        result = self.session.get(self.HOME_URL, verify=False)

        html = HTML(html=result.text)

        if html.find('title', first=True).text == '我的京东':
            return True
        else:
            return False

    def load_cookie(self):
        if os.path.exists(self.COOKIE_PATH):
            with open(self.COOKIE_PATH, 'r') as f:
                cookies = f.read()
            cookies = json.loads(cookies)
            cookies = requests.utils.cookiejar_from_dict(
                cookies, cookiejar=None, overwrite=True)
            self.session.cookies = cookies
            return True
        return False


class Login(base):

    def login(self):
        ''' selenium 登录京东 '''

        if self.load_cookie() and self.check_login():
            return True

        cookies = openWithWebBrowser(self.LOGIN_URL)
        with open(self.COOKIE_PATH, 'w') as f:
            f.write(json.dumps(cookies))

        if self.load_cookie() and self.check_login():
            return True

        return False
