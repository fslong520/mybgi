#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 660e '

__author__ = 'fslong'

import sys

import pyquery
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class Render(QWebEngineView):
    def __init__(self, url):
        self.html = None
        self.app = QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.load(QUrl(url))
        while self.html is None:
            self.app.processEvents(QEventLoop.ExcludeUserInputEvents |
                                   QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
        self.show()
        self.app.quit()

    def _callable(self, data):
        self.html = data

    def _loadFinished(self, result):
        self.page().toHtml(self._callable)


def render(url):
    """Fully render HTML, JavaScript and all."""
    htmlPage = Render(url).html
    PQPage = pyquery.PyQuery(htmlPage)
    return PQPage
if __name__=='__main__':
    a=render('https://xueqiu.com/')
    b=a('.home__timeline__item').items()
    for i in b:
        print('%s\n%s\n'%(i('a').text(),i('p').text()))