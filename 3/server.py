"""Программа-сервер"""
import argparse
import socket
import sys
import json

import logging
import threading
import time

import logs.server_log_config
from logs.dec_log import log
from common.desk import DeskPortCheck
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSE, MSG, SENDER, MESSAGE_TEXT, RESPONSE_200, \
    RESPONSE_400, DESTINATION, EXIT
from common.utils import get_message, send_message
from metaclasses import ServerMaker
from main_db import Database

SERVER_LOGGER = logging.getLogger('server')


class Server(threading.Thread, metaclass=ServerMaker):
    def __init__(self, message, messages_list, client, clients, names, db):
        self.message = message
        self.client = client
        self.clients = clients
        self.messages_list = messages_list
        self.names = names
        self.db = db
        super().__init__()


    def mainloop(self):
        try:
            if '-p' in sys.argv:
                listen_port = int(sys.argv[sys.argv.index('-p') + 1])
                SERVER_LOGGER.info(listen_port)
                print(listen_port)
            else:
                listen_port = DEFAULT_PORT
                SERVER_LOGGER.info(listen_port)
                print(listen_port)
            if listen_port < 1024 or listen_port > 65535:
                SERVER_LOGGER.error('ValueError')
                raise ValueError
        except IndexError:
            SERVER_LOGGER.error('После параметра -\'p\' необходимо указать номер порта.')
            print('После параметра -\'p\' необходимо указать номер порта.')
            sys.exit(1)
        except ValueError:
            SERVER_LOGGER.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            sys.exit(1)

            # Затем загружаем какой адрес слушать

        try:
            if '-a' in sys.argv:
                listen_address = sys.argv[sys.argv.index('-a') + 1]
            else:
                listen_address = ''

        except IndexError:
            SERVER_LOGGER.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            print(
                'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            sys.exit(1)

            # Готовим сокет

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((listen_address, listen_port))
        transport.settimeout(0.5)

        clients = []
        messages = []
        names = dict()

        transport.listen(MAX_CONNECTIONS)

        while True:
            try:
                client, client_address = transport.accept()
            except OSError as err:
                print(err.errno)
                pass
            else:
                SERVER_LOGGER.info((f'Установлено соедение с ПК {client_address}'))
                clients.append(client)

            recv_data_lst = []
            send_data_lst = []

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        Server.process_client_message(get_message(client_with_message),
                                                      messages, client_with_message, clients, names)
                    except Exception:
                        SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                           f'отключился от сервера.')
                        clients.remove(client_with_message)

            for i in messages:
                try:
                    process_message(i, names, send_data_lst)
                except Exception:
                    SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                    clients.remove(names[i[DESTINATION]])
                    del names[i[DESTINATION]]
            messages.clear()


    @log
    def process_client_message(self):
        '''
        Обработчик сообщений от клиентов, принимает словарь -
        сообщение от клинта, проверяет корректность,
        возвращает словарь-ответ для клиента

        :param message:
        :return:
        '''
        # SERVER_LOGGER.info(f'Разбор сообщения от клиента : {message}')
        # if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
        #         and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        #     return {RESPONSE: 200, MSG: 'соединение установлено'}
        # return {
        #     RESPONDEFAULT_IP_ADDRESSE: 400,
        #     ERROR: 'Bad Request'
        # }
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {self.message}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in self.message and self.message[ACTION] == PRESENCE and \
                TIME in self.message and USER in self.message:
            # Если такой пользователь ещё не зарегистрирован,
            # регистрируем, иначе отправляем ответ и завершаем соединение.
            if self.message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[self.message[USER][ACCOUNT_NAME]] = self.client
                send_message(self.client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя пользователя уже занято.'
                send_message(self.client, response)
                self.clients.remove(self.client)
                self.client.close()
            return
        # Если это сообщение, то добавляем его в очередь сообщений.
        # Ответ не требуется.
        elif ACTION in self.message and self.message[ACTION] == MSG and \
                DESTINATION in self.message and TIME in self.message \
                and SENDER in self.message and MESSAGE_TEXT in self.message:
            self.messages_list.append(self.message)
            return
        # Если клиент выходит
        elif ACTION in self.message and self.message[ACTION] == EXIT and ACCOUNT_NAME in self.message:
            self.clients.remove(self.names[self.message[ACCOUNT_NAME]])
            self.names[self.message[ACCOUNT_NAME]].close()
            del self.names[self.message[ACCOUNT_NAME]]
            return
        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            send_message(self.client, response)
            return

@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    listen_port = DeskPortCheck()

    # # проверка получения корректного номера порта для работы сервера.
    # if not 1023 < listen_port < 65536:
    #     SERVER_LOGGER.critical(
    #         f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. '
    #         f'Допустимы адреса с 1024 до 65535.')
    #     sys.exit(1)
    #
    return listen_address, listen_port

@log
def process_message(message, names, listen_socks):

    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')

@log
def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    '''
    Server.mainloop(arg_parser())

    # Загрузка параметров командной строки, если нет параметров, то задаём значения по умолчанию.
    listen_address, listen_port = arg_parser()

    # Инициализация базы данных
    database = Database()

    # Создание экземпляра класса - сервера и его запуск:
    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    def print_help():
        print(f'+++++')

    # Основной цикл сервера:
    while True:
        command = input('Введите команду: ')
        if command == 'help':
            print_help()
        elif command == 'exit':
            break
        elif command == 'users':
            for user in sorted(database.users_list()):
                print(f'Пользователь {user[0]}, последний вход: {user[1]}')
        elif command == 'connected':
            for user in sorted(database.active_users_list()):
                print(
                    f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, время установки соединения: {user[3]}')
        elif command == 'loghist':
            name = input('Введите имя пользователя для просмотра истории. '
                         'Для вывода всей истории, просто нажмите Enter: ')
            for user in sorted(database.login_history(name)):
                print(f'Пользователь: {user[0]} время входа: {user[1]}. Вход с: {user[2]}:{user[3]}')
        else:
            print('Команда не распознана.')


if __name__ == '__main__':
    main()
