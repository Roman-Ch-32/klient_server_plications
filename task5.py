# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
# и преобразовать результаты из байтовового в строковый тип на кириллице.

import platform
import subprocess
from chardet import detect

urls = ['yandex.ru', 'youtube.com']
code = '-n' if platform.system().lower() == 'windows' else '-c'

for url in urls:
    args = ['ping', code, '4', url]
    YA_PING = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in YA_PING.stdout:
        result = detect(line)
        print(result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
