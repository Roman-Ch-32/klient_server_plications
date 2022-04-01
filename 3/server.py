"""Программа-сервер"""

import socket
import sys
import json

import logging
import logs.server_log_config

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSE, MSG
from common.utils import get_message, send_message

SERVER_LOGGER = logging.getLogger('server')

def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    SERVER_LOGGER.info(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200, MSG: 'соединение установлено'}
    return {
        RESPONDEFAULT_IP_ADDRESSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    '''

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


    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_cient = get_message(client)
            SERVER_LOGGER.info(message_from_cient)
            print(message_from_cient)
            response = process_client_message(message_from_cient)
            send_message(client, response)
            SERVER_LOGGER.info(response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.critical('Принято некорретное сообщение от клиента.')
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()