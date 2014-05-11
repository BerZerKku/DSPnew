# -*- coding: utf-8 -*-
'''
Created on 10 май 2014г.

@author: Хозяин
'''

import unittest
import dsp

#------------------------------------------------------------------------------

class TestDsp(unittest.TestCase):
    """${short_summary_of_testcase}
    """

    #
    def setUp(self):
        ''' (self) -> None
        
            Создание класса dsphex перед каждым тестом.
        '''
        self.dsphex = dsp.DSPhex()

    #
    def tearDown(self):
        ''' (self) -> None
        
            Удаление dsphex после каждого теста
        '''
        self.dsphex = None

    #
    def testStr(self):
        """ (self) -> None
        
            Проверка результата работы функции класса __str__.
        """
        vers = u"Версия файла dsp.py %s" % dsp.VERSION
        self.assertEqual(unicode(self.dsphex), vers)

    #
    def testGetDevices(self):
        """(self) -> None
        
            Проверка результата работы функции класса getDevices.
        """
        devices = [u'Р400', u'Р400м', u'РЗСК']
        self.assertEqual(self.dsphex.getDevices(), devices)

    #
    def testSetDevice(self):
        """(self) -> None
        
            Проверка результата работы функции класса setDevice.
        """
        # установка Р400
        self.assertEqual(self.dsphex.setDevice(u'Р400'), u'Р400')
        # установка Р400м
        self.assertEqual(self.dsphex.setDevice(u'Р400м'), u'Р400м')
        # установка РЗСК
        self.assertEqual(self.dsphex.setDevice(u'РЗСК'), u'РЗСК')

        # неизвестное имя устройства
        self.assertRaises(ValueError, self.dsphex.setDevice, u'R400')

    #
    def testGetVersions(self):
        """ (self) -> None
        
            Проверка результата работы функции класса getVersions.
        """
        # неизвестное имя устройства
        self.assertEqual(self.dsphex.getVersions(u'R400'), [])
        # список для устройства по умолчанию == Р400
        vers = ['1v36', '1v34c', '1v30']
        self.assertEqual(self.dsphex.getVersions(), vers)
        # список для Р400
        vers = ['1v36', '1v34c', '1v30']
        self.assertEqual(self.dsphex.getVersions(u'Р400'), vers)
        # список для устройства по умолчанию == Р400
        self.assertEqual(self.dsphex.getVersions(), vers)
        # список для Р400м
        vers = ['1v34']
        self.assertEqual(self.dsphex.getVersions(u'Р400м'), vers)
        # список для РЗСК
        vers = ['1v30']
        self.assertEqual(self.dsphex.getVersions(u'РЗСК'), vers)

    #
    def testSetVersion(self):
        """(self) -> None
        
            Проверка результата работы функции класса setVersion.
        """
        # установка версии для устройства по умолчанию == для Р400
        self.assertEqual(self.dsphex.setVersion('1v34c'), '1v34c')
        # установка версии для Р400
        self.dsphex.setDevice(u'Р400')
        self.assertEqual(self.dsphex.setVersion('1v30'), '1v30')
        # установка версии для Р400м
        self.dsphex.setDevice(u'Р400м')
        self.assertEqual(self.dsphex.setVersion('1v34'), '1v34')
        # установка версии для РЗСК
        self.dsphex.setDevice(u'РЗСК')
        self.assertEqual(self.dsphex.setVersion('1v30'), '1v30')

        # неизвестная версия прошивки
        self.assertRaises(ValueError, self.dsphex.setVersion, '1v29')

    #
    def testSetFrequence(self):
        """(self) -> None
        
            Проверка результата работы функции класса setFrequence.
        """
        # минимальная частота
        min_freq = 16
        # максимальная частота
        max_freq = 1000

        # проверка установки минимального значения частоты
        self.assertEqual(self.dsphex.setFrequence(min_freq), min_freq)
        # проверка установки максимального значения частоты
        self.assertEqual(self.dsphex.setFrequence(max_freq), max_freq)
        # проверка установки промежуточной частоты
        self.assertEqual(self.dsphex.setFrequence(731), 731)
        # проверка установки частоты заданной строкой
        self.assertEqual(self.dsphex.setFrequence("87"), 87)
        # проверка установки частоты заданной 'float'
        self.assertEqual(self.dsphex.setFrequence(19.4), 19)

        # ошибочный тип данных на входе
        self.assertRaises(TypeError, self.dsphex.setFrequence, "87.28")
        # выход за диапазон вниз
        self.assertRaises(ValueError, self.dsphex.setFrequence, min_freq - 1)
        # выход за диапазон вверх
        self.assertRaises(ValueError, self.dsphex.setFrequence, max_freq + 1)

    #
    def testSetNumber(self):
        """(self) -> None
        
            Проверка результата работы функции класса setNumber.
        """
        # минимальный номер аппарата
        min_num = 1
        # максимальный номер аппарата
        max_num = 2

        # проверка установки минимального значения частоты
        self.assertEqual(self.dsphex.setNumber(min_num), min_num)
        # проверка установки максимального значения частоты
        self.assertEqual(self.dsphex.setNumber(max_num), max_num)
        # проверка установки промежуточной частоты
        self.assertEqual(self.dsphex.setNumber(2), 2)
        # проверка установки частоты заданной строкой
        self.assertEqual(self.dsphex.setNumber("1"), 1)
        # проверка установки частоты заданной 'float'
        self.assertEqual(self.dsphex.setNumber(2.3), 2)

        # ошибочный тип данных на входе
        self.assertRaises(TypeError, self.dsphex.setNumber, "1.2")
        # выход за диапазон вниз
        self.assertRaises(ValueError, self.dsphex.setNumber, min_num - 1)
        # выход за диапазон вверх
        self.assertRaises(ValueError, self.dsphex.setNumber, max_num + 1)