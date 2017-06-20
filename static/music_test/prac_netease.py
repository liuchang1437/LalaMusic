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

count = [1]
count[0] = 0

Header = {
    'Referer' : 'http://music.163.com',
    'Host' : 'music.163.com',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate'
}

Header1 = {
    'Referer' : 'http://music.163.com',
    'Host' : 'music.163.com',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate'
}

Header2 = {
    'Referer' : 'http://music.163.com',
    'Host' : 'music.163.com',
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate'
}

Header3 = {
    'Referer' : 'http://music.163.com',
    'Host' : 'music.163.com',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate'
}

Header_MP3 = {
    'Referer' : 'http://tools.hbtech.ml',
    'Host' : 'tools.hbtech.ml',
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate'
}

BASE_URL = 'http://music.163.com'
LYRIC_API = 'http://music.163.com/api/song/media?id='
MP3_API = 'http://tools.hbtech.ml/163music/mp3.php?id='

_session = requests.session()
_session.headers.update(Header)
#_session.proxies = {'http': 'http://203.91.121.76:3128'}
_session_mp3 = requests.session()
_session_mp3.headers.update(Header_MP3)

def get_page():
    #page_url = 'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=40&offset='+page_index
    list_record = []
    f = open('record.txt', 'rb')
    list_record = pickle.load(f)
    f.close()
    print(list_record)

    for i in range(20, 42):
        page_index = i * 35
        page_url = 'http://music.163.com/discover/playlist/?offset=' + str(page_index)
        soup = BeautifulSoup(_session.get(page_url).content, "lxml")
        song_list = soup.findAll('a', attrs = {'class':'tit f-thide s-fc0'})
        print("page url is:", page_url)
        for i in song_list:
            #print(i['href'])
            if(i['href'] in list_record):
                print('song list url :', i['href'], 'in record')
                continue
            else:
                print('song list url is:', i['href'])

                list_record.append(i['href'])
                f = open('record.txt', 'wb')
                pickle.dump(list_record, f)
                f.close()

                try:
                    get_playlist(i['href'])
                except:
                    print("catch an error")
                    time.sleep(20)
                    continue
                # a = random.randint(1,4)
                # if(a == 1):
                #     _session.headers.update(Header)
                # elif(a == 2):
                #     _session.headers.update(Header1)
                # elif(a == 3):
                #     _session.headers.update(Header2)
                # elif(a == 4):
                #     _session.headers.update(Header3)

            time.sleep(2)


def get_playlist(playlist_link):
    playlist_url = BASE_URL + playlist_link
    soup = BeautifulSoup(_session.get(playlist_url).content, "lxml")
    song_list = soup.find('ul', attrs = {'class':'f-hide'})
    #print(song_list)
    for i in song_list.findAll('li'):
        #print((i.find('a'))['href'])
        get_songinfo((i.find('a'))['href'])

def get_num_comments(song_id):
    Headers = {
        'Host': 'music.163.com',
        'Connection': 'keep-alive',
        'Content-Length': '484',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cookie': 'JSESSIONID-WYYY=b66d89ed74ae9e94ead89b16e475556e763dd34f95e6ca357d06830a210abc7b685e82318b9d1d5b52ac4f4b9a55024c7a34024fddaee852404ed410933db994dcc0e398f61e670bfeea81105cbe098294e39ac566e1d5aa7232df741870ba1fe96e5cede8372ca587275d35c1a5d1b23a11e274a4c249afba03e20fa2dafb7a16eebdf6%3A1476373826753; _iuqxldmzr_=25; _ntes_nnid=7fa73e96706f26f3ada99abba6c4a6b2,1476372027128; _ntes_nuid=7fa73e96706f26f3ada99abba6c4a6b2; __utma=94650624.748605760.1476372027.1476372027.1476372027.1; __utmb=94650624.4.10.1476372027; __utmc=94650624; __utmz=94650624.1476372027.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    Params = {
        'csrf_token': ''
    }

    Data = {
        'params': 'Ak2s0LoP1GRJYqE3XxJUZVYK9uPEXSTttmAS+8uVLnYRoUt/Xgqdrt/13nr6OYhi75QSTlQ9FcZaWElIwE+oz9qXAu87t2DHj6Auu+2yBJDr+arG+irBbjIvKJGfjgBac+kSm2ePwf4rfuHSKVgQu1cYMdqFVnB+ojBsWopHcexbvLylDIMPulPljAWK6MR8',
        'encSecKey': '8c85d1b6f53bfebaf5258d171f3526c06980cbcaf490d759eac82145ee27198297c152dd95e7ea0f08cfb7281588cdab305946e01b9d84f0b49700f9c2eb6eeced8624b16ce378bccd24341b1b5ad3d84ebd707dbbd18a4f01c2a007cd47de32f28ca395c9715afa134ed9ee321caa7f28ec82b94307d75144f6b5b134a9ce1a'
    }

    r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_'+ str(song_id), \
    headers=Headers, params=Params, data=Data)
    #print(r.json())
    #print("Comments:", r.json()['total'])
    return r.json()['total']

def get_mp3(song_id):
    song_url = MP3_API + song_id
    soup = BeautifulSoup(_session_mp3.get(song_url).content, "lxml")
    #print(soup)
    #print(soup.find('a', attrs = {'href':re.compile(".*\.mp3")}).string)
    #print(soup.find('a', attrs = {'href':re.compile(".*\.jpg")}).string)
    return soup.find('a', attrs = {'href':re.compile(".*\.mp3")}), \
    soup.find('a', attrs = {'href':re.compile(".*\.jpg")})

def get_songinfo(song_link):
    song_dict = {'SongID':'', 'SongName':'', 'Artist':'', 'Album':'', 'Lyric':'', 'Comments':'',\
    'Mp3Url':'', 'AlbumPic':''}
    song_id = song_link[song_link.index("=") + 1 :]
    comments_num = get_num_comments(song_id)
    if(comments_num > 200):
        #print("comments:", comments_num)
        count[0] = count[0] + 1
        song_dict['SongID'] = song_id
        song_url = BASE_URL + song_link
        lyric_url = LYRIC_API + song_id
        soup = BeautifulSoup(_session.get(song_url).content, "lxml")
        #print(soup.find('em', attrs = {'class':'f-ff2'}).string)
        song_dict['SongName'] = soup.find('em', attrs = {'class':'f-ff2'}).string
        artist = soup.find('a', attrs = {'class':'s-fc7', 'href':re.compile("^(/artist)((?!:).)*$")})
        if(artist != None):
            #print(soup.find('a', attrs = {'class':'s-fc7', 'href':re.compile("^(/artist)((?!:).)*$")}).string)
            song_dict['Artist'] = artist.string
        #print(soup.find('a', attrs = {'class':'s-fc7', 'href':re.compile("^(/album)((?!:).)*$")}).string)
        album = soup.find('a', attrs = {'class':'s-fc7', 'href':re.compile("^(/album)((?!:).)*$")})
        if(artist != None):
            song_dict['Album'] = album.string
        lyric = BeautifulSoup(_session.get(lyric_url).content, "lxml")
        try:
            lyric_json = json.loads(lyric.get_text())
        except:
            return
        if 'lyric' in lyric_json:
            #print(lyric_json['lyric'])
            song_dict['Lyric'] = lyric_json['lyric']
        song_dict['Comments'] = comments_num

        mp3_link, album_link = get_mp3(song_id)
        if(mp3_link != None):
            song_dict['Mp3Url'] = mp3_link.string
        if(album_link != None):
            song_dict['AlbumPic'] = album_link.string

        #print(song_dict)
        f = open(song_id + ".json", 'w', encoding="utf-8")
        json.dump(song_dict,f)
        f.close()
        print("num of songs crawed :", count[0])
    #str = input("请输入：");
    if(count[0] == 13000):
        sys.exit(0)
    time.sleep(2)

get_page()
