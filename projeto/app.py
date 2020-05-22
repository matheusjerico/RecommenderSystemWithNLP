from flask_pymongo import PyMongo
from flask import Flask

app = Flask("DesafioBigData")

app.config['MONGO_DBNAME'] = 'db_bigdata'
app.config['MONGO_URI'] = "mongodb://mongodb:27017/db_bigdata"

mongo = PyMongo(app)

