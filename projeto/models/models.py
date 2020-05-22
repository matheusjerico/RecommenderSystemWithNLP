from logger.logging_file import log
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
from models.database import write_mongo, read_mongo, delete_mongo, find_one_url
import pandas as pd
import numpy as np
from app import mongo


def data_insert(user, url):
    url_insert = find_one_url(url)

    if not url == url_insert:
        log.info("Inserindo URL e Usuário na Base de dados.")
        new_url = url.replace('.', ' ').replace('/', ' ').replace('-', ' ')
        new_row = {"user": user, "url": url, "new_url": new_url.lower()}
        write_mongo(new_row)
    else:
        log.warning("URL e Usuário já estão cadastrados na Base de Dados.")


def td_idf(dataframe):
    tf = TfidfVectorizer(analyzer='word',
                         ngram_range=(1, 3),
                         lowercase=True,
                         stop_words=stopwords.words('portuguese'),
                         max_features=500)
    tfidf_matrix = tf.fit_transform(dataframe['new_url'])

    return tfidf_matrix


def cosine_similarity(dataframe, tfidf_matrix):
    results = {}
    cos_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    for idx, row in dataframe.iterrows():
        similar_indices = cos_sim[idx].argsort()[:-100:-1]
        similar_items = [(cos_sim[idx][i],
                          dataframe['id'][i]) for i in similar_indices]
        results[row['id']] = similar_items[1:]

    return results


def recommendation(url_id, dataframe):
    list_url = []
    tfidf_matrix = td_idf(dataframe)
    results = cosine_similarity(dataframe, tfidf_matrix)
    recs = results[url_id][:10]
    for rec in recs:
        dataframe[dataframe['id'] == rec[1]]['url'].tolist()[0]
        new_row = {"url": dataframe[dataframe['id'] == rec[1]]['url'].tolist()[0],
                   "score": np.around(rec[0], decimals=3)}
        list_url.append(new_row)

    return list_url


def make_recommendation(url):
    log.info("Construindo recomendações.")
    url_recommendation = find_one_url(url)
    try:
        if not url == url_recommendation:
            log.info("URL não existe na Base de dados.")
            data_insert(user=None, url=url)

    except AttributeError as e:
        log.warning("Dataframe não existe. {}".format(e))
        data_insert(user=None, url=url)

    dataframe = read_mongo()
    dataframe.reset_index(inplace=True, drop=True)
    dataframe['id'] = dataframe.index
    url_id = int(dataframe[dataframe['url'] == url]['id'].values)
    list_url = recommendation(url_id=url_id, dataframe=dataframe)
    log.info("Recomendação finalizada.")

    return list_url


def delete_all():
    log.info("Deletando todos os registros.")
    number_of_url = delete_mongo()
    log.info("{} registros deletados.".format(number_of_url))
