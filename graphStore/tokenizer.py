#! /usr/bin/env python
#parseNoun text to sentences, proper per sense, freequency count of all nounse founs, remove trivial nouns
import operator
from collections import OrderedDict
import json
import nltk 
import sys
import csv
from nltk.corpus import brown, stopwords
   
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
            else if(token[1])
    return nouns
    
def 


if __name__ == '__main__':
    text = open(sys.argv[1],'r')
    mapping = parseNoun(text)
    writeOut = open(sys.argv[2],'w' )
    lis  = [(key,mapping[key]) for key in sorted(mapping,key=lambda key: mapping[key], reverse=True)]
    writeOut.write(json.dumps(lis))
    writeOut.write("/n")
    writeOut.close()
