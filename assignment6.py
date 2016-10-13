from __future__ import division
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import string
import nltk

# Tycho Koster, David Stap, Jeroen Terstall

if __name__ == '__main__':
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

    DutchStop = stopwords.words('dutch')

    BoW = Counter([w for w in nltk.word_tokenize(allvragen) if not w in set(DutchStop)])
    # show the top 20 most used words
    BoW.most_common(20)


    V = list(BoW)
    conprob = {}
    # Concatenate text
    text = []
    for c in range(len(normalized_ministerie)):
        text.append([])
        prior_c = normalized_ministerie[c]
        ministerie = kvrdf.ministerie.value_counts().keys()[c]
        for d in range(len(kvrdf.ministerie)):
            if(ministerie == kvrdf.ministerie[d]):
                text_document = kvrdf.titel[d].translate(str.maketrans({key: None for key in string.punctuation}))
                text[c].append(text_document)
    print([Counter(nltk.word_tokenize(text_c)) for text_c in text])
