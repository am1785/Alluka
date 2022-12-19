import os
import sys
import json
from . import db

sys.path.append("Soara/")

from flask import Flask, jsonify, redirect, render_template
from flask_restful import Api, Resource
from config import Config
# from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.getenv("SECRET_KEY")
    api = Api(app)
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # flask --app Soara init-db
    # flask --app Soara --debug run

    # a simple page that says hi
    @app.route('/hello')
    def hi():
        return 'Hi!'

    @app.route('/index')
    def index():
        return render_template('index.html')

# restful implementation of Flask API

    class SearchResult(Resource):
        def get(self, q, random):
            cursor = db.get_db()
            select_query = 'SELECT COUNT(*) FROM corpus WHERE text LIKE ?;'
            count = cursor.execute(
            select_query,
            ('% '+q+' %',)).fetchone()

            if random==1:
                select_query = 'SELECT text FROM corpus WHERE text LIKE ? ORDER BY RANDOM() LIMIT 10;'
            else:
                select_query = 'SELECT text FROM corpus WHERE text LIKE ? LIMIT 10;'
            result = cursor.execute(
            select_query,
            ('% '+q+' %',)).fetchall()
            result = [tuple(row) for row in result]
            result.append(tuple(count))
            db.close_db()
            return jsonify(result)

    api.add_resource(SearchResult, "/search/q=<string:q>&r=<int:random>")

    # NATIVE implementation of REST API
    # @app.route('/search/q=<string:q>', methods=['GET'])
    # # protect against injections: https://github.com/TryGhost/node-sqlite3/issues/57
    # def search_corpus(q):
        # cursor = db.get_db()
        # count = cursor.execute(
        # 'SELECT COUNT(*) FROM corpus WHERE text LIKE ?;',
        # ('% '+q+' %',)).fetchone()

        # result = cursor.execute(
        # 'SELECT text FROM corpus WHERE text LIKE ? ORDER BY RANDOM() LIMIT 10;', 
        # ('% '+q+' %',)).fetchall()
        # result = [tuple(row) for row in result]
        # result.append(tuple(count))
        # db.close_db()
        # return jsonify(result)

    # adding regexp implementation: https://github.com/thomasnield/oreilly_intermediate_sql_for_data/issues/5

    return app