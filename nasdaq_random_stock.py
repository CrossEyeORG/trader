import random
import time
from ftplib import FTP
from io import BytesIO


NUMBER_OF_RETRIES = 10
SLEEP_IN_SECONDS = 1
class Nasdaq:
    def __init__(self):
        self.__data = self.download()
        self.stock_list = self.format(self.__data)
    def download(self):
        count = 0
        data = BytesIO()
        while True:
            try:
                with FTP('ftp.nasdaqtrader.com') as ftp:
                    ftp.login()
                    ftp.retrbinary('RETR /SymbolDirectory/nasdaqlisted.txt', data.write)
            except:
                if count == NUMBER_OF_RETRIES:
                    raise Exception(f'Failed to download source after {count} retries.')
                else:
                    sleep = (SLEEP_IN_SECONDS * 2 ** count + random.uniform(0, 1))
                    time.sleep(sleep)
                    count += 1
                    continue
            data.seek(0)
            return data.read().decode()
    def format(self, data):
        out = []
        buff = []
        for c in data:
            if c == '\n':
                _stock = ''.join(buff).split('|')[0]
                if not "." in _stock:
                    out.append(_stock)
                    buff = []
            else:
                buff.append(c)
        else:
            if buff:
                out.append(''.join(buff))
        out.pop(0)
        out.pop(len(out)-1)
        return out
    def get_random_stock(self):
        return random.choice(self.stock_list) 

s = Nasdaq()
s.get_random_stock()
