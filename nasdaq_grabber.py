from ftplib import FTP
from io import BytesIO


class Nasdaq:
    def __init__(self):
        self.__data = self.download()
        self.stock_list = self.format(self.__data)
    def download(self):
        data = BytesIO()
        with FTP('ftp.nasdaqtrader.com') as ftp:
            ftp.login()
            ftp.retrbinary('RETR /SymbolDirectory/nasdaqlisted.txt', data.write)
        
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
        print(out)
        return out

s = Nasdaq()
