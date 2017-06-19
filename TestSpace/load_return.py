import pickle
import json

f = open('returned.dat', 'rb')
dict_list = pickle.load(f)
f.close()

#song_dict = {'SongID':'', 'SongName':'', 'Artist':'', 'Album':'', 'Lyric':'', 'Comments':'',\
#    'Mp3Url':'', 'AlbumPic':''}

#for i in dict_list:
#    print(i['SongID'], '-', i['SongName'], '-', i['Artist'],'-', i['Album'],'-', i['Mp3Url'], '-', i['AlbumPic'])
i = dict_list[0]
print(i['SongID'], '-', i['SongName'], '-', i['Artist'],'-', i['Album'],'-', i['Mp3Url'], '-', i['AlbumPic'])
i = dict_list[1]
print(i['SongID'], '-', i['SongName'], '-', i['Artist'],'-', i['Album'],'-', i['Mp3Url'], '-', i['AlbumPic'])
i = dict_list[11]
print(i['SongID'], '-', i['SongName'], '-', i['Artist'],'-', i['Album'],'-', i['Mp3Url'], '-', i['AlbumPic'])
