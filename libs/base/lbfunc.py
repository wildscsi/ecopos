_author__ = 'BM'
# -*- coding: utf-8 -*-
import copy                   # Для копирования словарей
import datetime               # Библиотека работы с датой и временем
import time                   # Библиотека работы со временем
import decimal    as decimal  # Для работы с округлениеми
import importlib  as imp      # Для динамического импортирования модулей

# ===== ЧИСЛОВЫЕ =====
# Округление
def mround(n1,p1=2):
    c1 = '0.00'
    if type(n1) is str: n1 = 0
    if   p1 == 0: c1 = '0'
    elif p1 == 1: c1 = '.0'
    elif p1 == 2: c1 = '.00'
    elif p1 == 3: c1 = '.000'
    elif p1 == 4: c1 = '.0000'
    elif p1 == 5: c1 = '.00000'
    n2  = decimal.Decimal(n1).quantize(decimal.Decimal(c1), rounding=decimal.ROUND_HALF_UP)
    tn1 = type(n1)
    if tn1 is float:
        nres = float(n2)
    elif tn1 is int:
        nres = int(n2)
    else:
        nres = float(n2)
    return nres

# ===== ЧИСЛОВЫЕ =====
# Отображение числа с количеством нулей после запятой
def mformat(n1,p1=2,triad=True):
    if type(n1) is str: n1 = mval(n1,p1)
    cf = '%0.2f'
    if   p1 == 0: cf = '%0.0f'
    elif p1 == 1: cf = '%0.1f'
    elif p1 == 2: cf = '%0.2f'
    elif p1 == 3: cf = '%0.3f'
    elif p1 == 4: cf = '%0.4f'
    elif p1 == 5: cf = '%0.5f'
    cres = cf % n1
    if triad:
        ipos = cres.find('.')
        if ipos > 0:
            c1 = cres[0:ipos]; c2 = '.' + cres[ipos+1:]
        else:
            c1 = cres; c2 = ''
        c1 = ' ' * (15-len(c1)) + c1
        cres = c1[0:3] + ' ' + c1[3:6] + ' ' + c1[6:9] + ' ' + c1[9:12] + ' ' + c1[12:] + c2
        cres = cres.strip(' ')
    return cres

# ===== ЧИСЛОВЫЕ =====
# Преобразует строку к числу
def mval(s1='',r1=2):
    s1 = s1.strip(' ')
    zn = ''
    if len(s1) == 0:
        s1 = '0'
    else:
        if s1[0:1] == '-': zn = '-'; s1 = s1[1:]
        ipos = s1.find('.')
        if ipos > -1:
            if ipos + 1 == len(s1):
                s1 = s1[0:ipos]
                ipos = -1
        if ipos > -1:
            c1 = s1[0:ipos]; c2 = s1[ipos+1]
            if not (c1.isdigit() and c2.isdigit()):
                s1 = '0'
                if r1 > 0:
                    s1 = s1 + '.' + '0' * r1
        else:
            if not s1.isdigit(): s1 = '0'
    n1 = eval(zn + s1)
    return mround(n1,r1)

# ===== СТРОКОВЫЕ =====
# Возвращает строку дополненную пробелами слева, справа или слева и справа (по центру)
def pads(s1='',n1=10,tp='L',ch=' '):
    tp = tp.upper()
    if not tp in 'LRC': tp = 'L'
    if not type(s1) is str: s1 = str(s1)
    s1 = s1.strip(' ')
    n2 = len(s1)
    if n2 == 0: return ch * n1
    if n2 < n1:
        if tp == 'L':
            return ch * (n1 - n2) + s1
        elif tp == 'R':
            return s1 + ch * (n1 - n2)
        elif tp == 'C':
            n3 = int((n1 - n2) / 2)
            return ch * n3 + s1 + ch * (n1 - n2 - n3)
    else: return s1[0:n1]

# ===== СТРОКОВЫЕ =====
# Возвращает строку дополненную пробелами слева
def padl(s1,n1=10,ch=' '):
    return pads(s1,n1,'L',ch)

# ===== СТРОКОВЫЕ =====
# Возвращает строку дополненную пробелами справа
def padr(s1,n1=10,ch=' '):
    return pads(s1,n1,'R',ch)

# ===== СТРОКОВЫЕ =====
# Возвращает строку дополненную пробелами слева и справа (по центру)
def padc(s1,n1=10,ch=' '):
    return pads(s1,n1,'C',ch)

# ===== СТРОКОВЫЕ =====
# Проверяет пустая ли строка
def isempty(ctxt=''):
    ctxt = ctxt.strip(' ')
    if len(ctxt) == 0: return True
    return False

# ===== ДАТА и ВРЕМЯ =====
# Возвращает Дату-Время или значение
def get5dt(cres='ymd',nsec=0,dt=None):
    cres = cres.lower()
    if dt is None: dt = datetime.datetime.now()
    if not nsec == 0:
        dt = dt + datetime.timedelta(seconds=nsec)
    if cres == 'dmy':
        return dt.strftime("%d-%m-%Y %H:%M:%S")
    elif cres == 'ymd':
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    elif cres == 'dtos':
        return dt.strftime("%Y%m%d")
    elif cres == 'ttos':
        return dt.strftime("%Y%m%d%H%M%S")
    elif cres == 'time':
        return dt.strftime("%H:%M:%S")
    elif cres == 'date':
        return dt.strftime("%d-%m-%Y")
    elif cres == 'wday':
        return dt.isoweekday()
    elif cres == 'stamp':
        return '_' + '%X' % int(1000000*time.time())
    elif cres == 'nstamp':
        return int(1000000*time.time())
    elif cres == 'dtstamp':
        c1 = dt.strftime("%Y%m%d%H%M%S")
        l1 = []
        for i in range(len(c1)):
            if i in [2,4,6,8,10,12]: l1.append(c1[i:i+2])
        stamp = l1[0]
        for i in [1,2,3,4,5]:
            n1 = int(l1[i])
            if n1 < 10: stamp += str(n1)
            elif 9 < n1 < 36: stamp += chr(65 + n1 - 10)
            elif n1 > 35: stamp += chr(97 + n1 - 36)
        return stamp
    elif cres == 'seconds':
        return int((dt - dt.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
    else:
        return dt


# ===== ДАТА и ВРЕМЯ =====
# Проверяет, что символьное выражение является выражением Дата-Время
def chkdt(cdt=''):
    cdt  = cdt.strip(' ')
    if not len(cdt) == 19: return False
    p1 = cdt.split(' ')
    hour = 0; minute = 0; second = 0
    try:
        day  = int(p1[0][0:2]); month  = int(p1[0][3:5]); year   = int(p1[0][6:10])
        hour = int(p1[1][0:2]); minute = int(p1[1][3:5]); second = int(p1[1][6:8])
    except:
        year = 0; month = 0; day = 0
    if not (year > 0 and month > 0 and day > 0): return False
    lret = True
    try:
         datetime.datetime(year,month,day,hour,minute,second)
    except:
         lret = False
    return lret

# ===== ДАТА и ВРЕМЯ =====
# Сравнивает две даты, возвращают разницу в секундах
# Если 0 - даты совпадают, < 0 - 1-я дата меньше 2-й, > 0 - 1-я дата старше 2-й
def compdt(dt1=None,dt2=None):
    if dt1 is None: dt1 = datetime.datetime.now()
    if dt2 is None: dt2 = datetime.datetime.now()
    if dt1 == dt2: return 0
    elif dt1 > dt2:
        res = dt1-dt2
        return res.seconds
    else:
        res = dt2-dt1
        return -res.seconds

# ===== ДАТА и ВРЕМЯ =====
# Проверяет входит ли в диапазон ЧЧ:ММ-ЧЧ:ММ переданные ЧЧ:ММ
def intime(td='',tc=''):
    lf = True; t1=t2=t3=0.00
    try:
        p1 = td.split('-')
        t1 = float(p1[0].replace(':','.'))
        t2 = float(p1[1].replace(':','.'))
        t3 = float(tc.replace(':','.'))
    except:
        lf = False
    if not lf: return False
    if t2 > t1:
        if t1 <= t3 <= t2:
            return True
        else:
            return False
    else:
        if t1 <= t3 <= 24:
            return True
        elif t3 <= t2:
            return True
    return False

# ===== ДАТА и ВРЕМЯ =====
# Проверка на пустую дату.
# Признаком пустой является наличие 1900 года
def isempty_dt(dt1):
    if type(dt1) is datetime.datetime:
        if dt1.year == 1900: return True
        return False
    else:
        return True

# ===== ДАТА и ВРЕМЯ =====
# Аппаратная задержка sleep
def sleep(nsek = None):
    if nsek is None: nsek = 1
    time.sleep(nsek)

# ===== ЛИСТЫ и СЛОВАРИ =====
# Поиск в листе словарей по имени поля значения
# при успешном поиске возращается словарь, иначе None
def seek(allrec,fname,xvalue):
    for orec in allrec:
        for key, value in orec.items():
            if key == fname and value == xvalue:
                return orec
    return None

# Поиск позиции в листе
# возвращает номер позиции или -1 при неуспешном поиске
def lseek(lst,xvalue,ns=None,ne=None):
    lst = list(lst); imax = len(lst)
    if ns is None or ns < 0 or ns > imax: ns = 0
    if ne is None or ne < 0 or ne > imax: ne = imax
    try:
        iret = lst.index(xvalue,ns,ne)
    except:
        iret = -1
    return iret

# ===== СЛОВАРИ =====
# Преобразование строки вида словаря в словарь
def str2dict(ctxt=''):
    dret = None
    ctxt = ctxt.strip(' ')
    if not type(ctxt) is str: return None
    if not ctxt[0:1] == '{': ctxt = '{' + ctxt + '}'
    try:
        dret = eval(ctxt)
    except:
        pass
    return dret

# ===== СЛОВАРИ =====
# Полное копирование словаря
def dcopy(d1):
    return copy.deepcopy(d1)

# ===== КОНСТРУКТОР SQL выражений =====
# Сравнивает текущую запись из словаря со структурой таблицы
# и формирует выражение для записи в Postgre SQL
def getexprinsertpsql(rec,ctable='',cstruc='',efld='',inc1='',inc2='',ch="'",cret=";"):
    cinsert = ''; cvalue = ''
    for cfld in cstruc.split(';'):
        ipos    = cfld.find(' ')
        ctype   = cfld[ipos+1:30]
        ctype2  = ctype
        ctype   = ctype[0:4]
        cfld    = cfld[0:ipos]
        if len(efld) > 0:
            if efld == cfld: continue
        if inc1 == cfld and len(inc2) > 0:
            cinsert += ',' + cfld; cvalue += ',' + inc2
            continue
        if   ctype == 'inte':
            pvalue = str(rec[cfld])
        elif ctype == 'nume':
            pvalue = str(rec[cfld])
        elif ctype == 'char':
            ipos      = ctype2.find('(')
            ctype2    = ctype2[ipos+1:len(ctype2)]
            ilen      = int(ctype2[0:len(ctype2)-1])
            pvalue    = rec[cfld][0:ilen]
            pvalue    = ch + pvalue.replace("'",'"') + ch
        elif ctype == 'text':
            pvalue = ch + rec[cfld].replace("'",'"') + ch
        elif ctype == 'bool':
            pvalue = str(rec[cfld])
            if len(pvalue) == 0: pvalue = 'False'
        elif ctype == 'time':
            pvalue = ch + str(rec[cfld]) + ch
        elif ctype == 'date':
            pvalue = ch + str(rec[cfld]) + ch
        elif ctype == 'as_t':
            pvalue = ch + str(rec[cfld]) + ch
        else:
            continue
        cinsert += ',' + cfld
        cvalue  += ',' + pvalue
    cinsert = cinsert[1:len(cinsert)]
    cvalue = cvalue[1:len(cvalue)]
    return "INSERT " + "INTO " + ctable + "(" + cinsert + ") VALUES (" + cvalue + ")" + cret

# ===== КОНСТРУКТОР SQL выражений =====
# Возвращает выражение для WHERE дата1 и дата2 с разницей в днях
def getdtwheredays(nday=0,fname='dt',dt=None):
    if dt is None: dt = datetime.datetime.now()
    dte = get5dt('ymd',0,dt)[0:10] + ' 23:59:59'
    dt = dt - datetime.timedelta(days=nday)
    dts = get5dt('ymd',0,dt)[0:10] + ' 00:00:00'
    return fname + ">='" + dts + "' and " + fname + "<='" + dte + "'"

# ===== КОНСТРУКТОР SQL выражений =====
# Возвращает выражение для WHERE дата1 и дата2 с разницей в секундах
def getdtwheresec(nsec=0,fname='dt',dt=None):
    if dt is None: dt = datetime.datetime.now()
    dte = get5dt('ymd',0,dt)
    dts = get5dt('ymd',-nsec,dt)
    return fname + ">='" + dts + "' and " + fname + "<='" + dte + "'"

# ===== КОНСТРУКТОР SQL выражений =====
# Возвращает выражение для WHERE дата меньше выбранной даты
def getdtwherelessdays(nday=0,fname='dt',dt=None):
    if dt is None: dt = datetime.datetime.now()
    dt = dt - datetime.timedelta(days=nday)
    return fname + "<=" + get5dt('ymd',0,dt)[0:10] + ' 23:59:59'

# ===== КОНСТРУКТОР SQL выражений =====
# Преобразует словарь записи в словарь символьных значений
# в соответствии со структурой
def rec2str(rec, cstruc):
    orec = {}
    for cfld in cstruc.split(';'):
        ipos = cfld.find(' ')
        ctype = cfld[ipos + 1:30]
        ctype2 = ctype
        ctype = ctype[0:4]
        cfld = cfld[0:ipos]
        if rec.get(cfld) is None: continue
        if ctype == 'inte':
            orec[cfld] = str(rec[cfld])
        elif ctype == 'nume':
            orec[cfld] = str(rec[cfld])
        elif ctype == 'char':
            ipos = ctype2.find('(')
            ctype2 = ctype2[ipos + 1:len(ctype2)]
            ilen = int(ctype2[0:len(ctype2) - 1])
            orec[cfld] = rec[cfld][0:ilen]
        elif ctype == 'text':
            orec[cfld] = rec[cfld]
        elif ctype == 'bool':
            if rec[cfld]:
                orec[cfld] = 'True'
            else:
                orec[cfld] = 'False'
        elif ctype == 'time':
            orec[cfld] = get5dt('ymd',0,rec[cfld])
        else:
            continue
    return orec

# ===== ОБЪЕКТЫ =====
# Возвращает словарь, содержащий объект, созданный на основании
# библиотеки и модуля
def getobjclass(clib='',cname='',*args,**kwargs):
    dret            = dict()
    dret['ob']      = None
    dret['errmsg']  = ''
    dret['return']  = True
    try:
        module = imp.import_module(clib)
        klass = getattr(module,cname)
        dret['ob'] = klass(*args,**kwargs)
    except Exception as e:
        dret['errmsg'] = e.args[0]
        dret['return'] = False
    return dret

# ===== ОБЪЕКТЫ =====
# Перегружает библиотечный модуль
def objreload(clib=''):
    dret            = dict()
    dret['errmsg']  = ''
    dret['return']  = True
    try:
        imp.reload(clib)
    except Exception as e:
        dret['errmsg'] = e.args[0]
        dret['return'] = False
    return dret


def getxybutkey(**kwargs):
    ores = []
    xs = kwargs.get('x',0); y1 = kwargs.get('y',0); w1 = kwargs.get('w',68); h1 = kwargs.get('h',58)
    keys = kwargs.get('keys',[])
    x1 = xs
    for ckey in keys:
        if ckey == '\n':
            y1 += h1; x1 = xs; continue
        elif ckey == '\t':
            x1 += w1; continue
        else:
            ores.append({'x':x1,'y':y1,'key':ckey})
            x1 += w1
    return dcopy(ores)




