import glob
import json
import os.path
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

import jieba
from myanalyzer import ChineseAnalyzer, ChineseAnalyzer_LYRIC
# from whoosh.analysis import SimpleAnalyzer,LowercaseFilter,StopFilter,StemFilter
# from whoosh.analysis import Tokenizer,Token
# from whoosh.lang.porter import stem
# import jieba
# import re

# STOP_WORDS = frozenset(('a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can',
#                         'for', 'from', 'have', 'if', 'in', 'is', 'it', 'may',
#                         'not', 'of', 'on', 'or', 'tbd', 'that', 'the', 'this',
#                         'to', 'us', 'we', 'when', 'will', 'with', 'yet',
#                         'you', 'your', '的', '了', '和'))
# STOP_WORDS = frozenset((' '))
#
# STOP_WORDS_LYRIC = frozenset(('a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can',
#                         'for', 'from', 'have', 'if', 'in', 'is', 'it', 'may',
#                         'not', 'of', 'on', 'or', 'tbd', 'that', 'the', 'this',
#                         'to', 'us', 'we', 'when', 'will', 'with', 'yet',
#                         'you', 'your', '的', '了', '和'))
#
# accepted_chars = re.compile(r"[\u4E00-\u9FA5]+")
#
# class ChineseTokenizer(Tokenizer):
#     def __call__(self, text, **kargs):
#         words = jieba.tokenize(text, mode="search")
#         token = Token()
#         for (w,start_pos,stop_pos) in words:
#             if not accepted_chars.match(w) and len(w) < 1:
#                 continue
#             token.original = token.text = w
#             token.pos = start_pos
#             token.startchar = start_pos
#             token.endchar = stop_pos
#             yield token
#
# class ChineseTokenizer_LYRIC(Tokenizer):
#     def __call__(self, text, **kargs):
#         words = jieba.tokenize(text, mode="search")
#         token = Token()
#         for (w,start_pos,stop_pos) in words:
#             if not accepted_chars.match(w) and len(w) <= 1:
#                 continue
#             token.original = token.text = w
#             token.pos = start_pos
#             token.startchar = start_pos
#             token.endchar = stop_pos
#             yield token
#
# def ChineseAnalyzer(stoplist=STOP_WORDS, minsize=1, stemfn=stem, cachesize=50000):
#     return (ChineseTokenizer() | LowercaseFilter() |
#             StopFilter(stoplist=stoplist,minsize=minsize) |
#             StemFilter(stemfn=stemfn, ignore=None,cachesize=cachesize))
#
# def ChineseAnalyzer_LYRIC(stoplist=STOP_WORDS_LYRIC, minsize=1, stemfn=stem, cachesize=50000):
#     return (ChineseTokenizer_LYRIC() | LowercaseFilter() |
#             StopFilter(stoplist=stoplist,minsize=minsize) |
#             StemFilter(stemfn=stemfn, ignore=None,cachesize=cachesize))

analyzer = ChineseAnalyzer()
analyzer_LYRIC = ChineseAnalyzer_LYRIC()

schema = Schema(SongID=STORED,
                SongName=TEXT(stored=True, analyzer=analyzer),
#                Artist=TEXT(stored=True, field_boost=2.0, analyzer=analyzer),
                Artist=TEXT(stored=True, analyzer=analyzer),
                SearchContext=TEXT(stored=True, analyzer=analyzer),
                Album=STORED,
                Lyric=TEXT(stored=True, analyzer=analyzer_LYRIC),
                Comments=NUMERIC(stored=True),
                AlbumPic=STORED)

# for t in analyzer_LYRIC("you want to go to somewhere and playing football"):
#     print(t.text)

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
        SearchContext = song_info['SongName'] + ',' + song_info['Artist'],
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
