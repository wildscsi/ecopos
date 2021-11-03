__author__ = 'BM'
# -*- coding: utf-8 -*-
import os
from datetime import *

class WrLog:
    def __init__(self):
        self.nolog      = False
        self.logsize    = 1024*1024 # 1Mb = 1024*1024
        self.filename   = 'app'
        self.path       = ''
        self.errmsg     = ''

    def writelog(self, cmsg='', ch='-'):
        # log не ведём
        self.errmsg = ''
        if self.nolog: return
        # проверяем наличие файла
        if os.path.exists(self.path + self.filename + '.log'):
            # если размер файла больше заданного - переименновываем в OLD
            if os.path.getsize(self.filename + '.log') > self.logsize:
                try:
                    os.replace(self.path + self.filename + '.log', self.path + self.filename + '.old')
                except Exception as e:
                    return self.errbox('Ошибка переименовывания файла\n%s' %e)
        # открываем файл на дозапись
        ctxt = datetime.today().strftime("%d-%m-%Y %H:%M") + '\n' + cmsg + '\n' + ch * 50
        return self.datatofile(ctxt,self.filename + '.log','LOG')

    def datatofile(self,cmsg='',cfile='',atr='',cfld=None):
        self.errmsg = ''; atr = atr.upper()
        if 'NEW' in atr: self.delfile(cfile)
        if 'LOG' in atr: return self.fsave(cmsg,cfile)
        if len(cfile) == 0: return self.errbox('Имя файла не определено')
        tpv = type(cmsg)
        ctxt = '-' * 50 + '\n' + datetime.today().strftime("%d-%m-%Y %H:%M") + '\n'
        if tpv is str:
            if 'TXT' in atr: return self.fsave(cmsg,cfile)
            ctxt += 'ТИП STRING\n' + cmsg
        elif tpv is dict:
            ctxt += 'СЛОВАРЬ ДАННЫХ\n'
            if len(cmsg) == 0: return self.fsave('Словарь пуст',cfile)
            ctxt += self.getdict(cmsg,cfld)
        elif tpv is list:
            ipos = 0
            ctxt += 'СПИСОК ДАННЫХ\n'
            if len(cmsg) == 0: return self.fsave('Список пуст',cfile)
            cmsg = list(cmsg)
            for c1 in cmsg:
                if type(c1) is dict:
                    ipos += 1
                    ctxt += '< ' + str(ipos) + ' > ' + '-' * 10 + '\n' + self.getdict(c1,cfld)
                else:
                    ctxt += str(c1) + '\n'
        else:
            ctxt += 'ТИП ' + str(tpv).upper() + '\n' + str(cmsg)
        return self.fsave(ctxt,cfile)

    @staticmethod
    def getdict(dic1,cfld):
        if len(dic1) == 0: return 'Словарь пуст'
        ctxt = ''
        if not cfld is None: cfld += ','
        try:
            dic1 = dict(dic1)
            lst = dic1.keys()
            for ckey in lst:
                if not cfld is None:
                    if not ckey + ',' in cfld: continue
                ctxt += ckey + '=' + str(dic1[ckey]) + '\n'
        except Exception as e:
            ctxt = 'ОШИБКА DATATOFILE: запись словаря\n%s' %e
        return ctxt

    def delfile(self,cfile=''):
        if len(cfile) == 0: return self.errbox('Имя файла не определено')
        try:
            os.remove(cfile)
        except Exception as e:
            return self.errbox('ОШИБКА DELFILE: удаления файла\n%s' %e)
        return True

    # Пишит информацию в файл
    def fsave(self,cmsg='',fname='',cp='utf-8'):
        fname = fname.strip(' ')
        if len(fname) == 0:
            return self.errbox('Имя файла неопределено')
        try:
            ofile = open(fname, 'a', encoding=cp)
            ofile.write(cmsg + '\n')
            ofile.close()
        except Exception as e:
            return self.errbox('Ошибка записи в файл\n%s' %e)
        return True

    # Читает информацию из файла
    def fload(self,fname='',cp='utf-8'):
        fname = fname.strip(' '); lret = True; han = None; cresult = ''
        if len(fname) == 0:
            return self.errbox('Имя файла неопределено'),''
        if not os.path.isfile(fname):
            return self.errbox('Файл ' + fname.upper() + ' не найден'),''
        try:
            han = open(fname,'r',encoding=cp)
        except Exception as e:
            lret = self.errbox('Ошибка чтения из файла\n' + fname.upper() + '\n%s' %e),''
        if not lret: return False,''
        for line in han:
            cresult += line
        han.close()
        return True, cresult

    def errbox(self,cmsg):
        self.errmsg = 'WRLOG: ' + cmsg
        return False
