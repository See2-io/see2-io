import pandas as pd
import numpy as np
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


def top_tfidf_features(row, features, top_n=20):
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats, columns=['feature', 'score'])
    return df


def top_features_in_doc(X, features, row_id, top_n=25):
    row = np.squeeze(X[row_id].toarray())
    return top_tfidf_features(row, features, top_n)


def top_topics(df, tail=0.25, n=0.02):
    '''
    :param df: A :class: pandas.DataFrame containing text documents.
    :param tail: the percentage of df to take as df.tail(), i.e. use 'tail' % of the most recent documents.
    :param n: the percentage of top topics to return.
    :return: top_topics
    '''
    if 0.0 <= tail <= 1.0:
        df_tail = df.tail(round(len(df) * tail))
    else:
        df_tail = df.tail(round(len(df) * 0.25))
    stopwords = ENGLISH_STOP_WORDS.union(['ect', 'hou', 'com', 'recipient'])
    vec = CountVectorizer(stop_words=stopwords, lowercase=True,).fit(df['clean_body'])
    bag_of_feats = vec.transform(df_tail['clean_body'])
    sum_feats = bag_of_feats.sum(axis=0)
    feats_freq = [(word, sum_feats[0, idx]) for word, idx in vec.vocabulary_.items()]
    feats_freq = sorted(feats_freq, key=lambda x: x[1], reverse=True)
    top_topics = feats_freq[:round(len(feats_freq) * n)]
    return set(list(zip(*top_topics))[0])
