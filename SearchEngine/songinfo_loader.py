import glob
import json
import os.path
from jieba.analyse import ChineseAnalyzer
import pickle

# song_dict = {}
# for file_name in glob.glob('../music_test/*.json'):
#     f = open(file_name, 'r', encoding="utf-8")
#     song_info = json.load(f)
#     song_dict[song_info['SongID']] = song_info
#     print("add one song")

# f = open('song_dict.txt', 'rb')
# song_dict = pickle.load(f)
# f.close()

# f = open('../music_test/'+ '110410' + '.json', 'r', encoding="utf-8")
# song_info = json.load(f)
#
# print(song_info)

def return_songinfo(SongID):
    f = open('static/music_test/'+ SongID + '.json', 'r', encoding="utf-8")
    song_info = json.load(f)
    #print(song_info)
    return song_info

#print(return_songinfo('114389'))
