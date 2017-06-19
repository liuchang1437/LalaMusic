import glob
import json
import os.path
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from jieba.analyse import ChineseAnalyzer

analyzer = ChineseAnalyzer()

schema = Schema(SongID=STORED,
                SongName=TEXT(stored=True, analyzer=analyzer),
#                Artist=TEXT(stored=True, field_boost=2.0, analyzer=analyzer),
                Artist=TEXT(stored=True, analyzer=analyzer),
                Album=STORED,
                Lyric=TEXT(stored=True),
                Comments=NUMERIC(stored=True),
                AlbumPic=STORED)

if not os.path.exists("musicIndex"):
    os.mkdir("musicIndex")
ix = create_in("musicIndex", schema)
writer = ix.writer()

for file_name in glob.glob('../music_test/*.json'):
    f = open(file_name, 'r', encoding="utf-8")
    song_info = json.load(f)
    #print(song_info)
    #print("\n")
    #print("********************")
    #for t in analyzer(song_info['SongName']):
    #    print(t.text)
    writer.add_document(
        SongID = song_info['SongID'],
        SongName = song_info['SongName'],
        Artist = song_info['Artist'],
        Album = song_info['Album'],
        Lyric = song_info['Lyric'],
        Comments = song_info['Comments'],
        AlbumPic = song_info['AlbumPic']
    )

writer.commit()
print("Inverted Index Created!")
# searcher = ix.searcher()
# parser = QueryParser("SongName", schema=ix.schema)
# for keyword in ("You Are My Sunshine"):
#     q = parser.parse(keyword)
#     results = searcher.search(q, terms=True)
#     for hit in results:
#         print(hit)
#         print("-----------------")
#         print(hit.highlights("SongName"))
#         print(hit.matched_terms())
#         print("**********")
