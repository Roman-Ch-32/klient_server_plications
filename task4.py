# 4. Преобразовать слова «разработка», «администрирование», «protocol»,
# «standard» из строкового представления в байтовое и выполнить обратное
# преобразование (используя методы encode и decode).

my_list = ['разработка', 'администрирование', 'protocol', 'standard']
my_list_2 = []

for el in my_list:
    my_list2 = el.encode('utf-8')
    my_list_2.append(my_list2)
    print('*' * 50)
    print('type: ', type(my_list2))
    print(my_list2)
    print('length of variable in bytes: ', len(my_list2))

print('*' * 50)
print(f'словарь {my_list_2}')

for el in my_list_2:
    new_el = el.decode('utf-8')
    # my_list_2.append(my_list2)
    print('*' * 50)
    print('type: ', type(new_el))
    print(new_el)
    print('length of variable in bytes: ', len(new_el))
