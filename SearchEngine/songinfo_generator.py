import glob
import json
import os.path
from jieba.analyse import ChineseAnalyzer
import pickle

song_dict = {}
for file_name in glob.glob('../music_test/*.json'):
    f = open(file_name, 'r', encoding="utf-8")
    song_info = json.load(f)
    song_dict[song_info['SongID']] = song_info
    print("add one song")

f = open('song_dict.txt', 'wb')
pickle.dump(song_dict, f)
f.close()
