#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 660e '

__author__ = 'fslong'

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import pyquery


def render(url):
    """Fully render HTML, JavaScript and all."""

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
            self.app.quit()
            cookieStore = self.page().profile().cookieStore()
            print(cookieStore)

        def _callable(self, data):
            self.html = data

        def _loadFinished(self, result):
            self.page().toHtml(self._callable)

    return Render(url).html


resualt = render('www.baidu.com')

PQPage = pyquery.PyQuery(resualt)
a = input('q;uur ')
