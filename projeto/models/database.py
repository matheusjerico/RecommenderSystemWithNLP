from app import mongo
from logger.logging_file import log
import pandas as pd

def write_mongo(data):
    db_url = mongo.db.url
    user = data['user']
    url = data['url']
    new_url = data['new_url']
    db_url_id = db_url.insert({'user': user,
                               'url': url,
                               'new_url': new_url})


def read_mongo():
    db_url = mongo.db.url
    output = db_url.find()
    data = pd.DataFrame(list(output))

    return data


def find_one_url(url):
    db_url = mongo.db.url
    document = db_url.find_one({"url": str(url)})

    if document is None:
        return False
    else:
        return document['url']


def delete_mongo():
    db_url = mongo.db.url
    number_of_url = db_url.delete_many({})
    
    return number_of_url.deleted_count