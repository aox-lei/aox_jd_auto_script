# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl
import sys


class WebBrowser(QWebEngineView):
    cookies = {}

    def __init__(self, *args, **kwargs):
        super(WebBrowser, self).__init__(*args, **kwargs)

        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(
            self.onCookieAdd)
        self.loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self):
        return self.cookies

    def onCookieAdd(self, cookie):
        '''
        :param cookie: QNetworkCookie
        '''
        name = str(cookie.name().data(), encoding='utf-8')
        value = str(cookie.value().data(), encoding='utf-8')

        self.cookies[name] = value

    def get_cookies(self):
        return self.cookies


def openWithWebBrowser(url):
    app = QApplication([])
    view = WebBrowser()
    view.load(QUrl(url))
    view.show()
    app.exec_()
    cookies = view.get_cookies()
    return cookies
