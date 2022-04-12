import boto3
import json
import random
from ftplib import FTP
from io import BytesIO


AWS_REGION = 'us-west-2'
S3_BUCKET = 's3bucketname'
S3_OBJECT = 'stocks.json'

class Nasdaq:
    def __init__(self):
        self.s3 = boto3.resource('s3', region_name=AWS_REGION)
        self.stock_list = self.s3_download()
    def download_source(self):
        data = BytesIO()
        with FTP('ftp.nasdaqtrader.com') as ftp:
            ftp.login()
            ftp.retrbinary('RETR /SymbolDirectory/nasdaqlisted.txt', data.write)
        data.seek(0)
        return data.read().decode()
    def s3_download(self):
        s3_obj = self.s3.Object(S3_BUCKET, S3_OBJECT)
        file_content = s3_obj.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        return json_content
    def s3_upload(self):
        __data = self.download_source()
        stock_list = self.format(__data)
        s3_obj = self.s3.Object(S3_BUCKET, S3_OBJECT)
        s3_obj.put(Body=(bytes(json.dumps(stock_list).encode('UTF-8'))))
        return stock_list
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
