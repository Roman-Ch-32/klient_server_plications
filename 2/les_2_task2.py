# Создать функцию write_order_to_json(),
# в которую передается 5 параметров — товар (item),
# количество (quantity), цена (price), покупатель (buyer), дата (date).
# Функция должна предусматривать запись данных в виде словаря в файл orders.json.
# При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json()
# с передачей в нее значений каждого параметра.
import json

params = {
    'item': 'item',
    'quantity': 'количество',
    'price': 'цена',
    'buyer': 'покупатель',
    'date': 'дата',
}


def write_order_to_json(data):
    with open('orders.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


write_order_to_json(params)
