# -*- coding: utf-8 -*-

from kivy.properties import BooleanProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineIconListItem, MDList
from libs.translation import Translation
from libs.baseclass.buttonlib import _MDRaisedButton
from kivy.uix.relativelayout import RelativeLayout
import libs.applibs.equaction as equ
import os


class RallySettingsScreen(MDScreen):
    list_created = BooleanProperty(False)
    dialoglang = None
    dialogabout = None
    dialoglicence = None
    app = None
    def on_pre_enter(self):
        return

    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)

    # -------------------------------------------------- LANG -------------------------------------------------

    # диалог выбора языка
    def show_lang_dialog(self):
        def select_locale(name_locale):
            for locale in self.app.dict_language.keys():
                if name_locale == self.app.dict_language[locale]:
                    self.app.alang = locale
                    self.app.config.set('General', 'language', self.app.lang)
                    self.app.config.write()
        if not self.app.window_language:
            items = []; i=0
            for ilang in self.app.dict_language.keys():
                items.append(ItemConfirm(text=ilang.upper() +' ('+ self.app.dict_language[ilang] +')'))
                # отметка выбранного языка
                if self.app.lang == ilang:
                    items[i].ids.check.active = True
                else:
                    items[i].ids.check.active = False
                i+=1

            self.dialoglang = MDDialog(
                title=self.app.translation._("Выбор языка"),
                type="confirmation",
                md_bg_color=self.app.bcolor3,
                items = items,
                buttons=[
                    MDFlatButton(text=self.app.translation._('ОТМЕНА'),font_style="Button",on_release=self.dialoglang_close),
                    _MDRaisedButton(text=self.app.translation._('ДА'),font_style="Button", on_release=self.on_signup ),
                ],
            )
        self.dialoglang.open()
        #self.add_widget(self.app.keyboard)

    # кнопка закрытия
    def dialoglang_close(self, *args):
        self.dialoglang.dismiss(force=True)

    # подтверждение выбора языка
    def on_signup(self, *args):
        self.dialoglang_close()
        for item in self.dialoglang.items:
            if item.ids.check.active:
                # сохраняем значение на приложении и в настройках
                self.app.lang = item.text[0:2].lower()
                self.app.config.set('General', 'language', self.app.lang)
                self.app.config.write()
                self.app.translation = Translation(self.app.lang, 'ecopos', os.path.join(self.app.directory, 'data', 'locales'))
                # нужно дважды, не ошибка
                self.app.translation = Translation(self.app.lang, 'ecopos', os.path.join(self.app.directory, 'data', 'locales'))
                # устанавливаем язык для DLL
                equ.action({'class':'setvalue','name':'lang','value':self.app.lang})
                break

    # -------------------------------------------------------------- ABOUT -----------------------------------------------------
    def show_about_dialog(self):
        if not self.dialogabout:
            self.dialogabout = MDDialog(
                title="О программе",
                md_bg_color=self.app.bcolor3,
                text='[color=2196f3]Ecopos\n[color=adadad]Version: ' + self.app.version + '\nwww.cpv.by\nSerhio & Yra Bos',
                buttons=[MDFlatButton(text=self.app.translation._("OK"),font_style="Button",on_release=self.dialogabout_close),],
            )
        self.dialogabout.open()

    # кнопка закрытия
    def dialogabout_close(self, *args):
        self.dialogabout.dismiss(force=True)

    # -------------------------------------------------------------- LICENCE ---------------------------------------------------
    def show_licence_dialog(self):
        if not self.dialoglicence:
            self.dialoglicence = MDDialog(
                title="Лицензия",
                md_bg_color=self.app.bcolor3,
                text=''
                    '[color=adadad]This program [color=2196f3] Ecopos [color=adadad]for Horeca & Retail.'
                    '\nCopyright © 2020 CPV.BY'
                    '\n\n'
                    'COPYRIGHT'
                    '\n'
                    'Android, Windows and Linux Version - Commercial.'
                    'Unregistered version limited to no more than 100 products or dishes.'
                    '\n'
                    'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.'
                    '\n'
                    'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.'
                    '\n'
                    'IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
                    ,
                buttons=[MDFlatButton(text=self.app.translation._("OK"),font_style="Button",on_release=self.dialoglicence_close),],
            )
        self.dialoglicence.open()

    # кнопка закрытия
    def dialoglicence_close(self, *args):
        self.dialoglicence.dismiss(force=True)

# отметка чек-бокса при нажатии на название языка
class ItemConfirm(OneLineAvatarIconListItem):
    divider = None
    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False