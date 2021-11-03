#! /usr/bin/python3.5
# -*- coding: utf-8 -*-
#
# calclib.py
#
# расчёты
#

import time

import json
from kivy.clock import Clock
from datetime import datetime
from libs.base.lbfunc import mround

# расчёт стоимости чека
class Calc():
    app = None
    sticket = 0     # сумма строк чека
    sall = 0        # сумма к оплате
    irow = 0        # строк чека
    alldsc = 0      # общая скидка на чек %
    ealldsc = 0     # общая скидка на чек

    def __init__(self, app):
        #super(Calc, self).__init__(**kwargs)
        self.app = app


    # расчёт сумм
    def calc(self):
        self.clearsumm()
        for item in self.app.aticket:
            self.sticket += item['sr']
            #self.sall = self.sticket
            self.irow +=1
        self.sticket = mround(self.sticket,self.app.iround)
        if self.app.lalldsc:
            self.ealldsc = mround(self.sticket*self.app.alldsc/100,self.app.iround)
            self.sall = mround(self.sticket - self.ealldsc,self.app.iround)
        else:
            self.ealldsc = 0
            self.sall = self.sticket

    # обнуление сумм
    def clearsumm(self):
        self.sticket = 0
        self.sall = 0
        self.irow = 0
        self.alldsc = 0