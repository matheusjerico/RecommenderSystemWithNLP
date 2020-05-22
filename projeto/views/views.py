from app import app, mongo
from logger.logging_file import log
from models.models import data_insert
from models.models import make_recommendation
from models.models import delete_all
from flask import request, jsonify


@app.route("/<path:url>/view/", methods=['POST'])
def view(url):
    try:
        log.info("POST in /<path:url>/view/")
        user = request.form.get('user')
        data_insert(user, url)
        return jsonify(success=True), 201

    except Exception as e:
        log.error("POST in /<path:url>/view: {}".format(e))


@app.route("/<path:url>/similar/", methods=['GET'])
def similar(url):
    try:
        log.info("GET in /<path:url>/similar")
        df_rec = make_recommendation(url)
        return jsonify(df_rec), 200

    except Exception as e:
        log.error("GET in /<path:url>/similar: {}".format(e))
        return jsonify(sucess=False), 500


@app.route("/", methods=['DELETE'])
def delete():
    try:
        log.info("DELETE in /")
        delete_all()
        return jsonify(sucess=True), 200

    except Exception as e:
        log.error("DELETE in /: {}".format(e))
        return jsonify(success=False), 500
