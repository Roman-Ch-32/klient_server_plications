# 3. Определить, какие из слов «attribute», «класс», «функция», «type»
# невозможно записать в байтовом типе. Важно: решение должно быть универсальным, т.е.
# не зависеть от того, какие конкретно слова мы исследуем.

my_list = ('attribute', 'класс', 'функция', 'type')


for el in my_list:
    try:
        my_list_2 = eval(f"b'{el}'")
        print('*' * 50)
        print('type: ', type(my_list_2))
        print(my_list_2)
        print('length of variable in bytes: ', len(my_list_2))
    except SyntaxError:
        new_list = []
        new_list.append(el)
        print(f'нельзя забайтить {new_list}')
