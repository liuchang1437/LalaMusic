import requests
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import random
import json
import base64
from Crypto.Cipher import AES
import os
import json
import time
import sys
import pickle
import urllib
import glob

def Schedule(a,b,c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' %(per))

Header_MP3 = {
    'Referer' : 'http://tools.hbtech.ml',
    'Host' : 'tools.hbtech.ml',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate'
}

_session_mp3 = requests.session()
_session_mp3.headers.update(Header_MP3)

MP3_API = 'http://tools.hbtech.ml/163music/mp3.php?id='

download_record = []
#download_record.append('1000.mp3')
f = open('../music_download/download_record.txt', 'rb')
download_record = pickle.load(f)
f.close()
length = len(download_record)

for file_name in glob.glob('../music_test/*.json'):
    f = open(file_name, 'r', encoding="utf-8")
    song_info = json.load(f)
    if song_info['SongID'] in download_record:
        print(song_info['SongID'], "in record")
        continue
    else:
        download_record.append(song_info['SongID'])

        song_url = MP3_API + song_info['SongID']

        soup = BeautifulSoup(_session_mp3.get(song_url).content, "lxml")
        download_link = soup.find('a', attrs = {'href':re.compile(".*\.mp3")})
        if (download_link != None):
            #print(download_link.string)
            try:
                print("download", song_info['SongID'], "from", download_link.string)
                urllib.request.urlretrieve(download_link.string, '../music_download/' + song_info['SongID'] + '.mp3')
            except:
                print("Error happend. Try again.")
                time.sleep(5)
                soup = BeautifulSoup(_session_mp3.get(song_url).content, "lxml")
                download_link = soup.find('a', attrs = {'href':re.compile(".*\.mp3")})
                print("download", song_info['SongID'], "from", download_link.string)
                urllib.request.urlretrieve(download_link.string, '../music_download/' + song_info['SongID'] + '.mp3')
        length = length + 1
        print(length, " songs are downloaded.")
        f = open('../music_download/download_record.txt', 'wb')
        pickle.dump(download_record, f)
        f.close()
        #time.sleep(2)
