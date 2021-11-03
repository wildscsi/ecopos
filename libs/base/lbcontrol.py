#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivymd.uix.label import MDLabel
import os



# Базовый класс TextInput
# есть выравнивание

class TextInput_(TextInput):
    hinttext=u'подсказка'

    def __init__(self, **kwargs):
        super(TextInput_, self).__init__(**kwargs)
        self.bind(on_text=self.on_text)
        self.font_size = 24
        self.hint_text = self.hinttext
        self.multiline = False
        # перерасчёт расзмеров шрифта
        self.bind(pos=self.setting_function, size=self.setting_function)


    # размеры шрифта и выравнивание
    def setting_function(self, instance, value):
        if not self.multiline:
            instance.font_size = instance.height /2
            instance.padding = [5, (instance.height - instance.line_height ) / 2]



    # установка текста
    def settext(self, text):
        self.text = text
        self.redraw()

    # установка текста
    def sethinttext(self, text):
        self.hint_text = text
        aa = 123
        self.redraw()

    def on_touch_up(self, touch):
        #self.redraw()
        pass

    def on_select(self, *args):
        pass

    def on_text(self, instance, value):
        pass
        self.redraw()

    def redraw(self):
        self.width = self.width-1
        self.width = self.width+1
        #self.padding = [5, (self.height - self.line_height ) / 2]
        #self.padding = [5, (self.height - self.line_height ) / 2]
        aa = 123
        #self.padding_x = [10,10]
        #self.padding_y = [5, (self.height/2/2)]
        #self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        aa= 231
        pass



# Базовый класс TextInput
# есть выравнивание

class Button_(Button):
    autosize = True
    ksize = 0.4
    def __init__(self, **kwargs):
        super(Button_, self).__init__(**kwargs)
        if self.autosize:
            self.font_size = self.height*self.ksize


# Базовый класс Label
class Label_(Label):
    id = ''
    scale_factor = .9
    factor = dimension = None
    font_name="./assets/fonts/"+"RobotoCondensed-Light"

    def __init__(self, **kwargs):
        super(Label_, self).__init__(**kwargs)



    # изменение шрифта
    def on_texture_size(self, *args):

        try:
            if not self.factor:
                self.factor = [self.font_size / self.texture_size[0], self.font_size / self.texture_size[1]]

            self.font_size0 = self.size[0] * self.scale_factor * self.factor[0]
            self.font_size1 = self.size[1] * self.scale_factor * self.factor[1]

            if self.font_size0 < self.font_size1:
                self.font_size = self.font_size0
            else:
                self.font_size = self.font_size1
            #self.text_size=self.texture_size
        except ZeroDivisionError:
            pass

    def update(self):
        aa = 123
        pass


