import pandas as pd
import numpy as np
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS


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


def top_topics(df, n):
    '''
    :param docs: A :class: pandas.DataFrame containing text documents.
    :param n: the number of top topics to return.
    :return:
    '''
    stopwords = ENGLISH_STOP_WORDS.union(['ect', 'hou', 'com', 'recipient'])
    # tf_idf_vect = TfidfVectorizer(tokenizer=LemmaTokenizer(), lowercase=True, stop_words=stopwords, min_df=1)
    # X = tf_idf_vect.fit_transform(df['clean_body'])
    # tf_idf_features = tf_idf_vect.get_feature_names()
    count_vect = CountVectorizer(stop_words=stopwords, lowercase=True, max_features=n)
    # count_vect = CountVectorizer(tokenizer=LemmaTokenizer, lowercase=True, max_features=n)
    X_count = count_vect.fit_transform(df['clean_body'])
    count_features = count_vect.get_feature_names()

    # i = 0
    # # For each email, fetch the top features
    # top_features = {}
    # while i < X.shape[0]:
    #     email = df.iloc[i]
    #     t_feats = top_features_in_doc(X, tf_idf_features, i, n)
    #     top_features[str(email['id'])] = dict(zip(t_feats.feature, t_feats.score))
    #     i += 1

    # top_features = count_features[:10]
    return count_features
