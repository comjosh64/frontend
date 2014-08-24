#! /usr/bin/env python
#parseNoun text to sentences, proper per sense, freequency count of all nounse founs, remove trivial nouns
import operator
from collections import OrderedDict
import os
from os import path
import json
import nltk 
import sys
import csv
from nltk.corpus import brown, stopwords
from nltk.collocations import *
from neo4jrestclient.client import GraphDatabase

NEO4J_IP_ADDRESS = 'localhost:7474/db/data/'
def parseNoun( textfile ) : 
    #takes a file object returns frequency minus trivial nouns
    sentences = nltk.sent_tokenize(textfile.read().lower())
    words = [nltk.pos_tag(nltk.word_tokenize(sent)) for sent in sentences]
    nounClassSet= set(['NN','NNP','NNS','NP'])
    stopwordsSet = set(stopwords.words('english'))
    #nouns = [[token[0] for token in sents if token[1] in nounClassSet  and token[0] not in stopwordsSet] for sents in words]
    nouns = {}
    for sents in words :
        for token in sents :
            if (token[1] in nounClassSet and token[0] not in stopwordsSet ):
                key = token[0]
                if (key in nouns.keys()):
                    nouns[key] += 1
                else:
                    nouns[key] = 1
    return nouns
    
def makeColocations(document):
    # collocation trigrams
    trigram_measures =  nltk.collocations.BigramAssocMeasures()
    finder = TrigramCollocaionFinder.from_words(document)
    trigrams = finder.nbest(trigram_measures.pmi, 3)
    for tri in trigrams: 
        storeCollocations(tri)


def storeCollocations(trigram):
    gdb = GraphDatabase(NEO4J_IP_ADDRESS)
    gdb.nodes.create(token = trigram[0] )
    gdb.relationships.create(token = trigram[1] )
    gdb.nodes.create(token = trigram[2] )

def ingest(absolutePath):
    print os.listdir(absolutePath)
    for document in os.listdir(directory):
        print os.path.join(absolutePath,document)
        dirpath = os.path.join(absolutePath,document)
        if not os.path.isdir(dirpath):
            f = open(dirpath)
            text = f.read()
            makeColocations(text)


        


if __name__ == '__main__':
    directory = sys.argv[1]
    print sys.argv[1]
    ingest(os.path.normpath(directory))
    #mapping = parseNoun(text)
    #writeOut = open(sys.argv[2],'w' )
    #lis  = [(key,mapping[key]) for key in sorted(mapping,key=lambda key: mapping[key], reverse=True)]
    #writeOut.write(json.dumps(lis))
    #writeOut.write("/n")
    #writeOut.close()
