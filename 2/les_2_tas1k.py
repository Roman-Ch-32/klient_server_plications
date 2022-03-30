# 1. Задание на закрепление знаний по модулю CSV.
# Написать скрипт, осуществляющий выборку определенных
# данных из файлов info_1.txt, info_2.txt, info_3.txt
# и формирующий новый «отчетный» файл в формате CSV. Для этого:
# Создать функцию get_data(), в которой в цикле осуществляется
# перебор файлов с данными, их открытие и считывание данных.
# В этой функции из считанных данных необходимо с помощью регулярных
# выражений извлечь значения параметров «Изготовитель системы»,
# «Название ОС», «Код продукта», «Тип системы». Значения каждого
# параметра поместить в соответствующий список. Должно получиться
# четыре списка — например, os_prod_list, os_name_list, os_code_list,
# os_type_list. В этой же функции создать главный список для хранения
# данных отчета — например, main_data — и поместить в него названия столбцов
# отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения для этих столбцов также оформить в виде списка и
# поместить в файл main_data (также для каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
# В этой функции реализовать получение данных через вызов функции get_data(),
# а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().

import csv
import re

import chardet


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    os_prod_pattern = re.compile('Изготовитель системы:')
    os_name_pattern = re.compile('Название ОС:')
    os_code_pattern = re.compile('Код продукта:')
    os_type_pattern = re.compile('Тип системы:')
    headers = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]
    for i in range(3):
        file = f'info_{i+1}.txt'
        with open(file, "rb") as f:
            data = f.read()
            charset = chardet.detect(data)
            data = data.decode(charset["encoding"])
            lines_array = data.split("\n")
            for line in lines_array:
                if len(os_prod_pattern.split(line)) > 1:
                    os_prod_list.append(os_prod_pattern.split(line)[1].strip())

                if len(os_name_pattern.split(line)) > 1:
                    os_name_list.append(os_name_pattern.split(line)[1].strip())

                if len(os_code_pattern.split(line)) > 1:
                    os_code_list.append(os_code_pattern.split(line)[1].strip())

                if len(os_type_pattern.split(line)) > 1:
                    os_type_list.append(os_type_pattern.split(line)[1].strip())


    data_transformed = list(zip(os_prod_list, os_name_list, os_code_list, os_type_list))
    return [headers] + data_transformed


def write_to_csv(data):
    with open('result.csv', 'w', encoding="utf-8") as f:
        csv.writer(f).writerows(data)


write_to_csv(get_data())
