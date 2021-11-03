# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 CPV.BY
#
# For suggestions and questions:
# <7664330@gmail.com>
#
# LICENSE: Commercial

from kivymd.uix.navigationdrawer import  MDNavigationLayout, MDNavigationDrawer

class StartScreen(MDNavigationLayout):
    oApp= None
    pass
    aa = 45
    #def __init__(self, **kvargs):
    #    super(StartScreen, self).__init__(**kvargs)
    #    self.oApp = kvargs.get('oApp')
    #    aa = 243



    def on_enter(self, *args):
        a = 7
        #self.oApp = self.manager.oapp
        #self.loadgrid()