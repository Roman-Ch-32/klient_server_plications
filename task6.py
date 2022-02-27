# 6. Создать текстовый файл test_file.txt,
# заполнить его тремя строками: «сетевое программирование»,
# «сокет», «декоратор». Далее забыть о том,
# что мы сами только что создали этот файл и исходить из того,
# что перед нами файл в неизвестной кодировке.
# Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того,
# в какой кодировке он был создан.
from chardet import detect

my_list = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w') as f:
    for el in my_list:
        f.write(f'{el}\n')


with open('test_file.txt', 'rb') as f1:
    file1 = f1.read()
    detected = detect(file1)
    decoded = file1.decode(detected['encoding'])
    with open('test_file.txt', 'w', encoding='utf-8') as i:
        i.write(f'{decoded}')


with open('test_file.txt', 'r', encoding='utf-8') as f2:
    file2 = f2.read()
    for el in file2:
        print(f'{el}')
