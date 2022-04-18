import sys

import logging

SERVER_LOGGER = logging.getLogger('server')


class DeskPortCheck:
    def __set__(self, instance, port):
        if port is int and port >= 0:
            if not 1023 < port < 65536:
                SERVER_LOGGER.critical(
                    f'Попытка запуска сервера с указанием неподходящего порта {port}. '
                    f'Допустимы адреса с 1024 до 65535.')
                sys.exit(1)
            instance.__dict__[self.name] = port

        SERVER_LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта {port}. '
            f'значение порта не может быть отрицательными или дробным числом')
        # raise TypeError(f'значение порта не может быть отрицательными или дробным числом')
        sys.exit(1)

    def __set_name__(self, owner, name):
        self.name = name
