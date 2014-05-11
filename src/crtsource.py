# -*- coding: utf-8 -*-

##
#  @file      crtsource.py
#  @brief     Создание файла данных.
#  @details   Создается файл содержащий словарь с именем dict_name
#             в который помещается содержимое файлов папки path.
#             Написан на Python 2.7.
#  @version   1.00
#  @date      май 2014
#  @author    Щеблыкин М.В.

# дополнительные возможности
#  @pre       First initialize the system.
#  @bug       Не найдено
#  @warning   Improper use can crash your application
#  @copyright GNU Public License.

import os
import sys

def create_file():
    path = u'\data'
    dict_name = 'data'
    
    # расширение файлов данных
    EXT = '.dat'
    
    # путь к текущему файлу (удаляем из пути имя файла)
    DIR = sys.argv[0].replace('\crtsource.py', '') 
    
    # список файлов в указанной папке
    files = os.listdir(DIR + path)
    
    # копирование в словарь 'имя файла' : 'его содержимое' для всех 
    # файло имеющих расширение EXT
    source = {}
    for f in files:
        if EXT in f:
            source[f] = open(DIR + path + '\\' + f, 'rb').read()
    
    # сохранение словаря в файл
    f = open(DIR + path + u'\source.py',"wb")
    f.write(dict_name + ' = ' + str(source))
    f.close()
    
    

#------------------------------------------------------------------------------
if __name__ == '__main__':
    create_file()
    
    
