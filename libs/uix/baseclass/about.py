# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 CPV.BY
#
# For suggestions and questions:
# <7664330@gmail.com>
#
# LICENSE: Commercial

import webbrowser

from kivy.uix.screenmanager import Screen


class About(Screen):
    def open_url(self, instance, url):
        webbrowser.open(url)
