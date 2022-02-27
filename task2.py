# 2. Каждое из слов «class», «function», «method» записать в байтовом типе.
# Сделать это необходимо в автоматическом, а не ручном режиме,
# с помощью добавления литеры b к текстовому значению,
# (т.е. ни в коем случае не используя методы encode, decode или функцию bytes)
# и определить тип, содержимое и длину соответствующих переменных.

my_list = ['class', 'function', 'method']

for el in my_list:
    my_list_2 = eval(f"b'{el}'")
    print('*' * 50)
    print('type: ', type(my_list_2))
    print(my_list_2)
    print('length of variable in bytes: ', len(my_list_2))
