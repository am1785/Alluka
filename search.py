import requests
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from Soara.auth import login_required
from Soara.db import get_db

bp = Blueprint('search', __name__)
soara_endpoint = "http://127.0.0.1:5000/"

@login_required
@bp.route('/search/q=<string:q>&o=<string:random>', methods=['GET'])
def search_corpus(q, random):
    if request.method == 'GET':
        q = q.strip()
        cursor = get_db()
        select_query = 'SELECT COUNT(*) FROM corpus WHERE text LIKE ?;'
        count = cursor.execute(
        select_query,
        ('% '+q+' %',)).fetchone()
        count = str(tuple(count)[0]) + " Total Results for \'" + q + "\'."
        print(count)

        if random=='random':
            select_query = 'SELECT channel, text FROM corpus INNER JOIN videos ON corpus.vid = videos.vid WHERE text LIKE ? ORDER BY RANDOM() LIMIT 10;'
        else:
            select_query = 'SELECT channel, text FROM corpus INNER JOIN videos ON corpus.vid = videos.vid WHERE text LIKE ? LIMIT 10;'

        result = cursor.execute(
        select_query,
        ('% '+q+' %',)).fetchall()
        result = [tuple(row) for row in result]
        result.append([count])
        cursor.close()
        return result
    # return render_template('index.html')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    results = [("No results", "0 results returned")]
    if request.method == 'POST':
        query = request.form['query']
        random = 'fixed'
        if request.form.get('random'):
            random = request.form['random']
        # results = search_corpus(q=query, random=random)
        results = requests.get(soara_endpoint+"search/q="+query+"&o="+random).json()


    return render_template('index.html', results=results)