# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 CPV.BY
#
# For suggestions and questions:
# <7664330@gmail.com>
#
# LICENSE: Commercial

import webbrowser
from kivymd.theming import ThemableBehavior
from kivymd.uix.screen import MDScreen


class AboutScreen(ThemableBehavior, MDScreen):
    def open_url(self, instance, url):
        webbrowser.open(url)
