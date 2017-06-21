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
from whoosh import highlight
import jieba
import pickle
#from myanalyzer import ChineseAnalyzer, ChineseAnalyzer_LYRIC
from whoosh.lang.porter import stem

# from whoosh.lang.porter import stem
# from whoosh.analysis import SimpleAnalyzer,LowercaseFilter,StopFilter,StemFilter
# from whoosh.analysis import Tokenizer,Token
#
# import re

# STOP_WORDS = frozenset((' '))
#
# STOP_WORDS_LYRIC = frozenset(('a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can',
#                         'for', 'from', 'have', 'if', 'in', 'is', 'it', 'may',
#                         'not', 'of', 'on', 'or', 'tbd', 'that', 'the', 'this',
#                         'to', 'us', 'we', 'when', 'will', 'with', 'yet',
#                         'you', 'your', '的', '了', '和'))
#
# #accepted_chars = re.compile(r"[\u4E00-\u9FA5]+")
#
# class ChineseTokenizer(Tokenizer):
#     def __call__(self, text, **kargs):
#         accepted_chars = re.compile(r"[\u4E00-\u9FA5]+")
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
#         accepted_chars = re.compile(r"[\u4E00-\u9FA5]+")
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

def dosearch(input_query):
    #analyzer = ChineseAnalyzer()
    #analyzer_LYRIC = ChineseAnalyzer_LYRIC()

    #song_dict = {'SongID':'', 'SongName':'', 'Artist':'', 'Album':'', 'Lyric':'', 'Comments':'',\
    #    'Mp3Url':'', 'AlbumPic':''}

    # for t in analyzer("周杰伦"):
    #     print(t.text)
    #
    # seg_list = jieba.cut_for_search("周杰伦")
    # print(", ".join(seg_list))

    if os.path.exists("static/musicIndex"):
        ix = open_dir("static/musicIndex")
    else:
        print("cannot find musicIndex")
        return None

    #parser = QueryParser("SongName", schema=ix.schema)
    parser = QueryParser("SearchContext", schema=ix.schema, group=OrGroup.factory(0))
    mparser = MultifieldParser(["SongName", "Artist"], schema=ix.schema, group=OrGroup.factory(0.5))
    #mparser = MultifieldParser(["SongName", "Artist"], schema=ix.schema)
    parser.add_plugin(FuzzyTermPlugin())
    mparser.add_plugin(FuzzyTermPlugin())

    scores = sorting.ScoreFacet()
    comment = sorting.FieldFacet('Comments', reverse=True)
    songname = sorting.FieldFacet("SongName")

    input_query = stem(input_query)
    query = parser.parse(input_query)
    print("query is", query)

    #with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
    with ix.searcher() as searcher:
        results = searcher.search(query, limit=100, sortedby=[scores, comment, songname])
        #results = searcher.search(query, limit=None, sortedby=comment)
        return_results = []
        for hit in results:
            #print(len(hit))
            #print(hit[0])
            #print(hit['SongID'], '-', hit['SongName'], "-", hit['Artist'], "-", hit['Comments'])
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
        return return_results

def dosearch_lyric(input_query):
    if os.path.exists("static/musicIndex"):
        ix = open_dir("static/musicIndex")
    else:
        print("cannot find musicIndex")
        return None

    parser = QueryParser("Lyric", schema=ix.schema)
    input_query = stem(input_query)
    query = parser.parse(input_query)
    print("query is", query)

    with ix.searcher() as searcher:
        results = searcher.search(query, limit=100)
        #results.fragmenter = highlight.WholeFragmenter()
        #results.fragmenter = highlight.SentenceFragmenter()
        results.fragmenter = highlight.ContextFragmenter(surround=30)
        results.fragmenter.charlimit = None
        results.formatter = highlight.HtmlFormatter(tagname = 'font color="red"')
        results.order = highlight.SCORE
        #results = searcher.search(query, limit=None, sortedby=comment)
        return_results = []
        for hit in results:
            #print(len(hit))
            #print(hit[0])
            #print(hit['SongID'], '-', hit['SongName'], "-", hit['Artist'], "-", hit['Comments'])
            song_dict = {'SongID':'', 'SongName':'', 'Artist':'', 'Album':'', 'Lyric':'', 'Comments':'',\
                         'AlbumPic':'', 'Highlights':''}
            song_dict['SongID'] = hit['SongID']
            song_dict['SongName'] = hit['SongName']
            song_dict['Artist'] = hit['Artist']
            song_dict['Album'] = hit['Album']
            song_dict['Lyric'] = hit['Lyric']
            song_dict['Comments'] = hit['Comments']
            song_dict['AlbumPic'] = hit['AlbumPic']
            song_dict['Highlights'] = hit.highlights("Lyric", top = 1)
            return_results.append(song_dict)
        return return_results

# f = open('returned.dat', 'wb')
# pickle.dump(return_results, f)
# f.close()
# return_results = dosearch(input('Please Input: '))
# for hit in return_results:
#     print(hit['SongID'], '-', hit['SongName'], "-", hit['Artist'], "-", hit['Comments'])
