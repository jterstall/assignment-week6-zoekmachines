from __future__ import division
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd
import MySQLdb
import string
import nltk
import glob
import os
import re

# Tycho Koster, David Stap, Jeroen Terstall

if __name__ == '__main__':
    folder = "doc/KVR/"
    kvrdf= pd.read_csv('KVR.csv.gz',
                   sep='\t', encoding='utf-8',
                   index_col=0,
                   names=['jaar', 'partij','titel','vraag','antwoord','ministerie'])
    normalized_ministerie = kvrdf.ministerie.value_counts().head(10) / sum(kvrdf.ministerie.value_counts())

    # Join all titels of the questions together
    allvragen = '\n'.join(str(v) for v in list(kvrdf.titel))

    # remove punctuation
    allvragen = allvragen.translate(str.maketrans({key: None for key in string.punctuation}))

    # Tokenize and turn into a bag of words
    BoW = Counter(nltk.word_tokenize(allvragen))
    # show the top 20 most used words
    BoW.most_common(20)

    DutchStop= stopwords.words('dutch')

    BoW= BoW= Counter([w for w in nltk.word_tokenize(allvragen) if not w in set(DutchStop)])
    # show the top 20 most used words
    BoW.most_common(20)

    V = allvragen
    Nc = kvrdf.ministerie.value_counts().head(10)
    i=0
    conprob = {}
    for c in range(len(normalized_ministerie)):
        prior_c = normalized_ministerie[c]
        Nct = 0
        print(prior_c)
        for t in V:
            for d in range(len(kvrdf.titel)):
                if(kvrdf.ministerie.keys()[c] == kvrdf.ministerie[d]):
                    if(t in kvrdf.titel or t in kvrdf.vraag or t in kvrdf.antwoord):
                        Nct +=1
            conprob[kvrdf.ministerie.keys()[c]][t] = ((Nct+1)/(Nc[c] +2))
    print(conprob)
