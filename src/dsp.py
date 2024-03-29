﻿# -*- coding: utf-8 -*-

##
#  @file      dsp.py
#  @brief     Создание файлов прошивки DSP для АВАНТ Р400, Р400м, РЗСК, К400.
#  @details   Создание файла прошивки для для заданного типа аппарата, версии
#             прошивки, частоты и номера.
#
#             На данный момент имеются:
#                 - Р400
#                     -# 1v36
#                     -# 1v34c (режим совместимости, номер аппарата не важен)
#                     -# 1v30
#                 - Р400м
#                     -# 1v34
#                 - РЗСК
#                     -# 1v30
#
#  @version   1.03
#  @date      май 2014
#  @author    Щеблыкин М.В.

# дополнительные возможности
#  @pre       First initialize the system.
#  @bug       Не найдено
#  @warning   Improper use can crash your application
#  @copyright GNU Public License.

## Версия программы.
VERSION = u"1v03"

import sys
import os
import my_func
from data.source import data
#import dsp.data.source as data

#
def newP400_1v36(source, freq, num):
    ''' (str) -> sr

        Корректирует файл прошивки версии 1v36 для Р400 для указанной частоты
        и номера аппарата.
    '''
    #
    def calcFreq(freq):
        ''' (int) -> int
            
        Вычисление КС для заданной частоты. 
        '''
        return 16 * freq

    def calcCrc1(freq, num):
        ''' (int, int) -> int
            
        Вычисление КС для заданной частоты. 
        '''
        if (num == 1):
            crc = 64
        elif (num == 2):
            crc = -64
        return crc + 32 * freq

    def calcCrc2(freq, num):
        ''' (int, int) -> int
        
            Вычисление КС для заданной частоты и номера аппарата.
        '''
        if (num == 1):
            crc = -16
        elif (num == 2):
            crc = 16
        return crc + 8 * freq

    if not isinstance(source, str):
        raise TypeError(u"Ошибочный тип данных 'str'", unicode(type(source)))

    if not isinstance(freq, int):
        raise TypeError(u"Ошибочный тип данных 'freq'", unicode(type(freq)))

    if not isinstance(num, int):
        raise TypeError(u"Ошибочный тип данных 'num'", unicode(type(num)))


    # два байта  зависят от частоты
    fr = my_func.intToStrHex(calcFreq(freq), 4, "le").decode('hex')
    adr = my_func.strHexToInt('1BEB')
    source = source[:adr] + fr + source[adr + len(fr):]

    # два байта  зависят от частоты и номера аппарата
    crc1 = my_func.intToStrHex(calcCrc1(freq, num), 4, "le").decode('hex')
    adr = my_func.strHexToInt('57EC')
    source = source[:adr] + crc1 + source[adr + len(crc1):]

    # два байта  зависят от частоты и номера аппарата
    crc2 = my_func.intToStrHex(calcCrc2(freq, num), 4, "le").decode('hex')
    adr = my_func.strHexToInt('57EE')
    source = source[:adr] + crc2 + source[adr + len(crc2):]

    return source

#
def newP400_1v34c(source, freq, num):
    ''' (str, int, int) -> str

        Корректирует файл прошивки версии 1v34c для Р400 для указанной частоты.
        Номер аппарата не используется.
    '''

    #
    def calcFreq(freq):
        ''' (int) -> int
            
        Вычисление КС для заданной частоты. 
        '''
        return 32 * freq

    def calcCrc1(freq, num):
        ''' (int, int) -> int
            
        Вычисление КС для заданной частоты. 
        '''
        return 32 * freq

    def calcCrc2(freq, num):
        ''' (int, int) -> int
        
            Вычисление КС для заданной частоты и номера аппарата.
        '''
        return 8 * freq

    if not isinstance(source, str):
        raise TypeError(u"Ошибочный тип данных 'str'", unicode(type(source)))

    if not isinstance(freq, int):
        raise TypeError(u"Ошибочный тип данных 'freq'", unicode(type(freq)))

    if not isinstance(num, int):
        raise TypeError(u"Ошибочный тип данных 'num'", unicode(type(num)))


    # два байта по адресу '1CDC' зависят от частоты
    fr = my_func.intToStrHex(calcFreq(freq), 4, "le").decode('hex')
    adr = my_func.strHexToInt('1CDC')
    source = source[:adr] + fr + source[adr + len(fr):]

    # два байта по адресу '5845' зависят от частоты
    crc1 = my_func.intToStrHex(calcCrc1(freq, num), 4, "le").decode('hex')
    adr = my_func.strHexToInt('5845')
    source = source[:adr] + crc1 + source[adr + len(crc1):]

    # два байта по адресу '5847' зависят от частоты
    crc2 = my_func.intToStrHex(calcCrc2(freq, num), 4, "le").decode('hex')
    adr = my_func.strHexToInt('5847')
    source = source[:adr] + crc2 + source[adr + len(crc2):]

    return source

#
def newP400_1v30(source, freq, num):
    ''' (str, int, int) -> str

        Корректирует файл прошивки версии 1v30 для Р400 для указанной частоты
        и номера аппарата.
    '''
    # строка '57D0' вычисляется относительно частоты и номера аппарата
    # xx (crc1) (crc2) xx xx xx (crc1, crc2 - двухбайтные)
    # строка '1BD0' зависит от частоты
    # (fr) xx xx xx xx xx xx

    #
    def calcCrc1(freq, num):
        val = freq * 32
        if num == 1:
            val += 64
        elif num == 2:
            val -= 64
        else:
            print u"calcCrc1"
            print u"Значения кроме 1 и 2 не принимаются:", num, type(num)
            raise ValueError
        val = my_func.intToStrHex(val)
        while len(val) < 4:
            val = '0' + val
        val = val[2:] + val[:2]
        return val

    #
    def calcCrc2(freq, num):
        val = freq * 8
        if num == 1:
            val -= 16
        elif num == 2:
            val += 16
        else:
            print u"calcCrc2"
            print u"Значения кроме 1 и 2 не принимаются:", num, type(num)
            raise ValueError
        val = my_func.intToStrHex(val)
        while len(val) < 4:
            val = '0' + val
        val = val[2:] + val[:2]
        return val

    #
    def calcFreq(val):
        val = "%02x0" % val
        if len(val) < 4:
            val = '0' + val
        val = val[2:] + val[:2]
        return val.upper()

    if not isinstance(source, str):
        raise TypeError(u"Ошибочный тип данных 'str'", unicode(type(source)))

    if not isinstance(freq, int):
        raise TypeError(u"Ошибочный тип данных 'freq'", unicode(type(freq)))

    if not isinstance(num, int):
        raise TypeError(u"Ошибочный тип данных 'num'", unicode(type(num)))

    # строка '1BD0' зависит от частоты
    fr = calcFreq(freq).decode('hex')
    adr = my_func.strHexToInt('1BD0')
    source = source[:adr] + fr + source[adr + len(fr):]

    # строка '57D0' вычисляется относительно частоты и номера аппарата
    # xx (crc1) (crc2) xx xx xx (crc1, crc2 - двухбайтные)
    crc1 = calcCrc1(freq, num).decode('hex')
    crc2 = calcCrc2(freq, num).decode('hex')
    adr = my_func.strHexToInt('57D0') + 1
    source = source[:adr] + crc1 + crc2 + source[adr + len(crc1) + len(crc2):]

    return source

#
def newP400m_1v34(source, freq, num):
    ''' (str, int, int) -> str
        
        Корректирует файл прошивки версии 1v34 для Р400м для указанной частоты
        и номера аппарата.
    '''

    def calcCrc1(freq, num):
        ''' (int, int) -> int
            
        Вычисление КС для заданной частоты и номера аппарата. 
        '''
        if (num == 1):
            crc = 64
        elif (num == 2):
            crc = -64
        return crc + 32 * freq

    def calcCrc2(freq, num):
        ''' (int, int) -> int
        
            Вычисление КС для заданной частоты и номера аппарата.
        '''
        if (num == 1):
            crc = -16
        elif (num == 2):
            crc = 16
        return crc + 8 * freq

    def calcFreq(freq):
        ''' (int) -> int
        
            Вычисление значения для частоты.
        '''
        return 32 * freq

    if not isinstance(source, str):
        raise TypeError(u"Ошибочный тип данных 'str'", unicode(type(source)))

    if not isinstance(freq, int):
        raise TypeError(u"Ошибочный тип данных 'freq'", unicode(type(freq)))

    if not isinstance(num, int):
        raise TypeError(u"Ошибочный тип данных 'num'", unicode(type(num)))

    # два байта по адресу '1C49' зависят только от частоты
    fr = my_func.intToStrHex(calcFreq(freq), 4, "le").decode('hex')
    adr = my_func.strHexToInt('1C49')
    source = source[:adr] + fr + source[adr + len(fr):]

    # два байта по адресу '5892' зависят от частоты и номера аппарата
    crc1 = my_func.intToStrHex(calcCrc1(freq, num), 4, "le").decode('hex')
    adr = my_func.strHexToInt('5892')
    source = source[:adr] + crc1 + source[adr + len(crc1):]

    # два байта по адресу '5894' зависят от частоты и номера аппарата
    crc2 = my_func.intToStrHex(calcCrc2(freq, num), 4, "le").decode('hex')
    adr = my_func.strHexToInt('5894')
    source = source[:adr] + crc2 + source[adr + len(crc2):]

    return source

#
def newRZSK_1v30(source, freq, num):
    ''' (str, int, int) -> str
        
        Корректирует файл прошивки версии 1v30 для РЗСК для указанной частоты
        и номера аппарата.
    '''

    def calcCrc1(freq, num):
        ''' (int, int) -> int
            
        Вычисление КС для заданной частоты и номера аппарата. 
        '''
        if (num == 1):
            crc = -39
        elif (num == 2):
            crc = 38
        return crc + 32 * freq


    def calcCrc2(freq, num):
        ''' (int, int) -> int
        
            Вычисление КС для заданной частоты и номера аппарата.
        '''
        if (num == 1):
            crc = 9
        elif (num == 2):
            crc = -10
        return crc + 8 * freq


    def calcFreq(freq):
        ''' (int) -> int
        
            Вычисление значения для частоты.
        '''
        return 16 * freq


    if not isinstance(source, str):
        raise TypeError(u"Ошибочный тип данных 'str'", unicode(type(source)))

    if not isinstance(freq, int):
        raise TypeError(u"Ошибочный тип данных 'freq'", unicode(type(freq)))

    if not isinstance(num, int):
        raise TypeError(u"Ошибочный тип данных 'num'", unicode(type(num)))

    fr = my_func.intToStrHex(calcFreq(freq), 4, "le").decode('hex')
    adr = my_func.strHexToInt('4DE6')
    source = source[:adr] + fr + source[adr + len(fr):]

    crc1 = my_func.intToStrHex(calcCrc1(freq, num), 4, "le").decode('hex')
    adr = my_func.strHexToInt('7C1E')
    source = source[:adr] + crc1 + source[adr + len(crc1):]

    crc2 = my_func.intToStrHex(calcCrc2(freq, num), 4, "le").decode('hex')
    adr = my_func.strHexToInt('7C22')
    source = source[:adr] + crc2 + source[adr + len(crc2):]

    return source

#----------------------------------------------------------------------------

## Класс создания прошивки DSP АВАНТ.
class DSPhex():
    ## Данные для создания прошивок.
    #  Название аппарата задается на русском языке, для упорядочивания списка.
    #  'c' в версии прошивки Р400 означает работу в совместимости
    FIRMWARE = {
                    u'Р400' : { '1v36'  : ('P400_1v36' , newP400_1v36),
                                '1v34c' : ('P400_1v34c', newP400_1v34c),
                                '1v30'  : ('P400_1v30' , newP400_1v30)
                              },
                    u'Р400м': {
                                '1v34'  : ('P400m_1v34', newP400m_1v34)
                              },
                    u'РЗСК' : {
                                '1v30'  : ('RZSK_1v30' , newRZSK_1v30)
                              }
                }

    ## Путь для файлов исходных прошивок.
    DIR_DATA = "data/"
    ## Расширение файлов исходных прошивок.
    EXT_DATA = ".dat"
    ## Путь для сохранения файлов прошивок.
    DIR_HEX = "hex/"

    ## Максимальная частота.
    MAX_FREQ = 1000
    ## Минимальная частота.
    MIN_FREQ = 16

    #
    def __init__(self, freq=100, num=1, device=u'Р400', version='1v36'):
        ''' (self, int, int, str) -> None
            
            Конструктор.
            @param freq Частота.
            @param num Номер аппарата.
            @param device Тип аппарата.
            @param version Версия прошивки.
        '''
        ## Тип аппарата.
        self._device = device;
        ## Частота.
        self._freq = freq;
        ## Номер аппарата.
        self._num = num;
        ## Версия прошивки.
        self._version = version;
        ## Исходная прошивка
        self._source = None

        self.setFrequence(freq)
        self.setNumber(num)
        self.setDevice(device)

    #
    def __str__(self):
        ''' (self) -> str
            
            Встроенная функция.
            @return Версия программы.
        '''
        return u"Версия файла dsp.py %s" % VERSION

    #
    def getVersions(self, device=None):
        ''' (self, str) -> list of str
            
            Формирование списка версий прошивок доступных для заданного типа
            аппарата. Список упорядочен по убыванию.
            
            @param device Тип аппарата.
            @return Список версий прошивок.
        '''
        versions = []

        if device is None:
            device = self._device

        device = unicode(device)
        if self.FIRMWARE.has_key(device):
            versions = sorted(self.FIRMWARE[device], reverse=True)
        return versions

    #
    def setVersion(self, vers):
        ''' (self, str) -> str
            
            Установка версии прошивки.
            
            @param vers Версия прошивки.
            @return Установленная версию прошивки.
        '''

        if not self.FIRMWARE[self._device].has_key(vers):
            raise ValueError(u"Ошибочное значение переменной 'vers'.")

        self._version = vers
        return self._version

    #
    def setFrequence(self, freq):
        ''' (self, str or number) -> int

            Установка частоты .
            
            @param freq Частота в диапазоне [MIN_FREQ, MAX_FREQ]кГц.
            @see MIN_FREQ
            @see MAX_FREQ
            @return Установленная частота.
        '''
        # проверка полученного номера аппарата
        try:
            freq = int(freq)
        except:
            raise TypeError(u"Неверный тип переменной 'freq'.")

        if freq < self.MIN_FREQ or freq > self.MAX_FREQ:
            raise ValueError(u"Ошибочное значение переменной 'freq'.")

        self._freq = freq
        return self._freq

    #
    def setNumber(self, num):
        ''' (self, str/number) -> int

            Установка номера аппарата. 
            
            @param num Номер аппарата в диапазоне [1, 2].
            @return Установленный номер аппарата.
        '''
        # проверка полученной частоты аппарата
        try:
            num = int(num)
        except:
            raise TypeError(u"Неверный тип переменной 'num'.")

        if num < 1 or num > 2:
            raise ValueError(u"Ошибочное значение переменной 'num'.")

        self._num = num
        return self._num

    #
    def getDevices(self):
        ''' (self) -> list of str
        
        
            Формирование списка версий аппаратов, для которых можно сформировать
            прошивку, упорядоченный по возрастанию.
            
            @return Список версий аппатов.
        '''
        return sorted(self.FIRMWARE)

    #
    def setDevice(self, device):
        ''' (self, str) -> None
            
            Установка типа аппарата.
  
            @param device Версия аппарата.
            @return Установленная версию аппарата.
        '''
        device = unicode(device)
        if not device in self.FIRMWARE.keys():
            raise ValueError(u"Ошибочное значение переменной 'device'.")

        # в случае смены аппарата, установим последнюю версию прошивки для него

        if self._device != device:
            self._device = device
            self.setVersion(self.getVersions(device) [0])

        return self._device

    #
    def saveNewHEX(self, name=None):
        ''' (self, str) -> str

            Сохраниение файла прошивки с заданными параметрами. В случае если
            \a name не задано, сохраняется в текущий каталог с именем
            созданным на основе информации о версии прошивки, частоте и 
            номере аппарата.
            
            @param name Путь и(или) имя файла прошивки.
            @return Имя файла созданной прошивки.
        '''

        device = self._device
        freq = self._freq
        num = self._num
        vers = self._version

#         self.loadSourceHEX()
        data_hex = self.FIRMWARE[self._device][self._version][0]
        data_hex += '_' + str(self._num)
        data_hex += self.EXT_DATA
        self._source = data[data_hex]
    
        # вызов функции создания файла прошивки
        func = self.FIRMWARE[device] [vers] [1]
        try:
            source = func(self._source, freq, num)
        except Exception as inst:
            text = u"Ошибка вызова функции создания новой прошивки: "
            text += unicode(func)
            raise NameError(text)

        # формирование имени файла
        if name is None:
            name = unicode(self.DIR_HEX)
            name += "%s_%03d_%d.hex" % \
                (self.FIRMWARE[device] [vers] [0], freq, num)
        else:
            name = unicode(name)

        try:
            # создание папки для прошивок, в случае ее отсутствия
            if not os.path.exists(self.DIR_HEX):
                os.makedirs(self.DIR_HEX)

            # сохранение файла прошивки
            f = open(name, 'wb')
            f.write(source)
            f.close()
        except Exception as inst:
            raise IOError(inst)

        print u'Файл сохранен успешно', name
        return name

    #
    def loadSourceHEX(self):
        ''' (self) -> str

            Загрузка исходного файла прошивки.
            
            @return Имя исходного файла прошивки. 
        '''

        # выбор необходимого исходного файла прошивки
        name = self.DIR_DATA
        name += self.FIRMWARE[self._device][self._version][0]
        name += '_' + str(self._num)
        name += self.EXT_DATA

        try:
            name = unicode(name)
            f = open(name, 'rb')
            self._source = f.read()
        except:
            raise IOError(u"Ошибка открытия исходного файла прошивки.")

        return name



#-----------------------------------------------------------------------------
if __name__ == '__main__':
    ''' Создание файла прошивки с заданной частотой и номером. 
        По умолчанию будет создана прошивка Р400_1v36 100кГц-1.
        Ключи:
        -f[number] - частота [MIN_FREQ, MAX_FREQ]кГц, например -f100
        -n[number] - номер аппарата [1, 2], например -n2
        -d[name] - тип аппарата [Р400, РЗСК, К400], например -dP400
        -v[vers] - версия прошивки, например -v1v30
    '''

    dspHEX = DSPhex()

    # установка папаремтров заданных ключами
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg[:2] == '-f':
            dspHEX.setFrequence(arg[2:])
        elif arg[:2] == '-n':
            dspHEX.setNumber(arg[2:])
        elif arg[:2] == '-d':
            dspHEX.setDevice(arg[2:])
        elif arg[:2] == '-v':
            dspHEX.setFrequence(arg[2:])

    try:
        dspHEX.saveNewHEX()
    except:
        print u'Не удалось сохранить файл прошивки'
