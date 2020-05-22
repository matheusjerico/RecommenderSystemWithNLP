from app import app
from models.models import *
from views.views import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from logger.logging_file import log
import requests
import random

def ingest_data():
    log.info("Populando Base de dados.")
    url = 'http://globo.com'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features='html.parser')
    tags = soup.findAll('a')
    for i in range(len(tags)):
        link = tags[i]['href']
        url = urlparse(link)
        if len(url.path.split('/')) <= 2:
            continue
        data_insert(random.randint(1, 20), link)


if __name__ == '__main__':
    log.info("Run without Gunicorn")
    app.run(host='0.0.0.0', port=8080)

else:
    log.info("Run with Gunicorn")
    ingest_data()