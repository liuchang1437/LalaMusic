import glob
import json
import os.path
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.qparser import FuzzyTermPlugin
from whoosh.qparser import OrGroup
from whoosh import scoring
from whoosh import sorting
from whoosh.lang.porter import stem
import jieba
import pickle

from whoosh.analysis import SimpleAnalyzer,LowercaseFilter,StopFilter,StemFilter
from whoosh.analysis import Tokenizer,Token

import re

# STOP_WORDS = frozenset(('a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can',
#                         'for', 'from', 'have', 'if', 'in', 'is', 'it', 'may',
#                         'not', 'of', 'on', 'or', 'tbd', 'that', 'the', 'this',
#                         'to', 'us', 'we', 'when', 'will', 'with', 'yet',
#                         'you', 'your', '的', '了', '和'))
STOP_WORDS = frozenset((' '))

accepted_chars = re.compile(r"[\u4E00-\u9FA5]+")

class ChineseTokenizer(Tokenizer):
    def __call__(self, text, **kargs):
        words = jieba.tokenize(text, mode="search")
        token = Token()
        for (w,start_pos,stop_pos) in words:
            if not accepted_chars.match(w) and len(w) < 1:
                continue
            token.original = token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = stop_pos
            yield token

def ChineseAnalyzer(stoplist=STOP_WORDS, minsize=1, stemfn=stem, cachesize=50000):
    return (ChineseTokenizer() | LowercaseFilter() |
            StopFilter(stoplist=stoplist,minsize=minsize) |
            StemFilter(stemfn=stemfn, ignore=None,cachesize=cachesize))

analyzer = ChineseAnalyzer()
#analyzer = SimpleAnalyzer()
#okenizer = RegexTokenizer()

# for t in analyzer("song stemming looking something"):
#     print(t.text)
# song_dict = {'SongID':'', 'SongName':'', 'Artist':'', 'Album':'', 'Lyric':'', 'Comments':'',\
#    'Mp3Url':'', 'AlbumPic':''}
#
# for t in analyzer("周杰伦"):
#     print(t.text)
#
# seg_list = jieba.cut_for_search("周杰伦")
# print(", ".join(seg_list))

if os.path.exists("musicIndex"):
    ix = open_dir("musicIndex")

#parser = QueryParser("SongName", schema=ix.schema, group=OrGroup.factory(0))
parser = QueryParser("SearchContext", schema=ix.schema, group=OrGroup.factory(0))
#parser = QueryParser("SongName", schema=ix.schema)
mparser = MultifieldParser(["SongName", "Artist"], schema=ix.schema, group=OrGroup.factory(0))
#mparser = MultifieldParser(["SongName", "Artist"], schema=ix.schema)
parser.add_plugin(FuzzyTermPlugin())
mparser.add_plugin(FuzzyTermPlugin())

scores = sorting.ScoreFacet()
comment = sorting.FieldFacet('Comments', reverse=True)
songname = sorting.FieldFacet("SongName")

#query = mparser.parse(stem(input("Please input: ")))
xxx = stem(input("Please input: "))
print("after steming:", xxx)
print("************************")
query = parser.parse(xxx)
print("query is", query)

#with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
with ix.searcher() as searcher:
    results = searcher.search(query, limit=100, sortedby=[scores, comment, songname])
    #results = searcher.search(query, limit=None, sortedby=scores)
    return_results = []
    for hit in results:
        #print(len(hit))
        #print(hit[0])
        print(hit.highlights("SearchContext"))
        print(hit['SongID'], '-', hit['SongName'], "-", hit['Artist'], "-", hit['Comments'])
        song_dict = {'SongID':'', 'SongName':'', 'Artist':'', 'Album':'', 'Lyric':'', 'Comments':'',\
                     'AlbumPic':''}
        song_dict['SongID'] = hit['SongID']
        song_dict['SongName'] = hit['SongName']
        song_dict['Artist'] = hit['Artist']
        song_dict['Album'] = hit['Album']
        song_dict['Lyric'] = hit['Lyric']
        song_dict['Comments'] = hit['Comments']
        song_dict['AlbumPic'] = hit['AlbumPic']
        return_results.append(song_dict)

# f = open('returned.dat', 'wb')
# pickle.dump(return_results, f)
# f.close()
