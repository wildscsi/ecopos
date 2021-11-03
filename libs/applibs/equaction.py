__author__ = 'BM'
# -*- coding: utf-8 -*-
# Вызов DLL работы с оборудованием

import ctypes as ctp
from kivymd.app import MDApp


def action(pdic, cbuff = None):
    try:
        app = MDApp.get_running_app()
        oequ  = ctp.CDLL(app.sodll)
        oequ.action.restype = ctp.c_bool
        oequ.action.argtypes = [ctp.c_char_p,ctp.c_char_p]
        n1 = 4096; n2 = n1
        if 'size1' in pdic: n1 = pdic['size1']
        if 'size2' in pdic: n2 = pdic['size2']
        buf1 = ctp.create_string_buffer(str(pdic).encode('utf-8'),n1)
        buf2 = cbuff
        if cbuff is None: buf2 = ''
        buf2  = ctp.create_string_buffer(buf2.encode('utf-8'),n2)
        lret  = oequ.action(buf1,buf2)
        dret  = eval(buf1.value.decode('utf-8'))
        vret  = buf2.value.decode('utf-8')
        # входной Json, входной буфер, выходной Json, выходной буфер, результат
        return pdic, cbuff, dret, vret, lret
    except:
        cbuff = {}
        cbuff['message'] = app.translation._('Ошибка доступа к оборудованию.')
        return False, False, cbuff, False, False

