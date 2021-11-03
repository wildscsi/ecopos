# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 CPV.BY
#
# For suggestions and questions:
# <7664330@gmail.com>
#
# LICENSE: Commercial

import os

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty

try:
    from kivymd.uix.button import MDFlatButton
except:
    raise ImportError("Install package KivyMD")


class BugReporter(FloatLayout):
    oApp = None
    title = StringProperty("Bug reporter")
    label_info_for_user = StringProperty("Error in the program!")
    info_for_user = StringProperty(
        "This bug will be reported after clicking the button below to help us fix it."
    )
    txt_report = StringProperty("Hello")
    report_readonly = BooleanProperty(False)
    icon_background = StringProperty("data/images/icon.png")

    def __init__(self, **kwargs):
        super(BugReporter, self).__init__(**kwargs)

    def _close(self, *args):
        from kivy.app import App

        App.get_running_app().stop()


Builder.load_string(
    """
<BugReporter>:
    txt_traceback: txt_traceback

    canvas:
        Color:
            rgba: 0, 1, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Image:
        source: root.icon_background
        opacity: 0.2

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)

        Label:
            id: title
            text: root.label_info_for_user
            text_size: self.size
            font_size: '20sp'
            halign: 'center'
            size_hint_y: None
            height: dp(50)

        Label:
            id: subtitle
            text: root.info_for_user
            text_size: self.size
            font_size: '14sp'
            halign: 'center'
            valign: 'top'
            size_hint_y: None
            height: dp(100)

        ScrollView:
            id: e_scroll
            scroll_y: 0

            TextInput:
                id: txt_traceback
                size_hint_y: None
                height: max(e_scroll.height, self.minimum_height)
                background_color: 1, 1, 1, 0.05
                text: root.txt_report
                foreground_color: 1, 1, 1, 1
                readonly: root.report_readonly

        BoxLayout:
            id: box_layout
            size_hint: 1, None
            padding: 5, 5
            height: dp(50)
            spacing: 2

            Button:
                text: "CLOSE and REPORT"
                on_release: root._close()

"""
)
