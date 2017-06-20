import glob
import json
import os.path
from jieba.analyse import ChineseAnalyzer

analyzer = ChineseAnalyzer()

for file_name in glob.glob('../music_test/*.json'):
    f = open(file_name, 'r', encoding="utf-8")
    song_info = json.load(f)
    print(song_info)
    print("\n")
    print("********************")
    for t in analyzer(song_info['SongName']):
        print(t.text)
    xxx = input("please input")
