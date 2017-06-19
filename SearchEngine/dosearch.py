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
from jieba.analyse import ChineseAnalyzer
import jieba
import pickle

def dosearch(input_query):
    analyzer = ChineseAnalyzer()

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

    parser = QueryParser("SongName", schema=ix.schema)
    mparser = MultifieldParser(["SongName", "Artist"], schema=ix.schema, group=OrGroup.factory(0.5))
    #mparser = MultifieldParser(["SongName", "Artist"], schema=ix.schema)
    parser.add_plugin(FuzzyTermPlugin())
    mparser.add_plugin(FuzzyTermPlugin())

    scores = sorting.ScoreFacet()
    comment = sorting.FieldFacet('Comments', reverse=True)
    songname = sorting.FieldFacet("SongName")

    query = mparser.parse(input_query)

    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        results = searcher.search(query, limit=None, sortedby=[scores, comment, songname])
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

# f = open('returned.dat', 'wb')
# pickle.dump(return_results, f)
# f.close()
