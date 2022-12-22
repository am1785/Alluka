import requests
import math
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from Soara.auth import login_required
from Soara.db import get_db

bp = Blueprint('search', __name__)
# soara_endpoint = "http://127.0.0.1:5000/"

@login_required
@bp.route('/search/<string:q>/<int:page>', methods=['GET', 'POST'])
def search_corpus(q, page):
    # print(request.args.get('string:q'))
    if request.method == 'GET':
        q = q.strip()
        print(f"searching for {q}")
        cursor = get_db()
        select_query = 'SELECT COUNT(*) FROM corpus WHERE text LIKE ?;'
        count = cursor.execute(
        select_query,
        ('% '+q+' %',)).fetchone()
        total_pages = int(math.ceil(int(tuple(count)[0]) / 30 + 0.01))
        pages = list(range(1, total_pages+1))

        print(f"total pages: {total_pages}")
        count = str(tuple(count)[0]) + " Total Results for \'" + q + "\'."
        offset = (page-1) * 30

        select_query = 'SELECT channel, text, videos.vid, CAST(timestamp as INTEGER) FROM corpus INNER JOIN videos ON corpus.vid = videos.vid WHERE text LIKE ? LIMIT 30 OFFSET ?;'

        result = cursor.execute(
        select_query,
        ('% '+q+' %', offset,)).fetchall()
        result = [tuple(row) for row in result]
        result.append([count])
        cursor.close()
        return render_template('index.html', results = result, pages = pages, params = q)

    if request.method == 'POST':
        print("recieved post from /search/<string:q>/<int:page> !")
        q = request.form['query']
        page = 1
        if request.form.get('page_no'):
            page = request.form['page_no']
        # return redirect(url_for("search.search_corpus", q=query, page=page))
        cursor = get_db()
        select_query = 'SELECT COUNT(*) FROM corpus WHERE text LIKE ?;'
        count = cursor.execute(
        select_query,
        ('% '+q+' %',)).fetchone()
        total_pages = int(math.ceil(int(tuple(count)[0]) / 30 + 0.01))
        pages = list(range(1, total_pages+1))

        count = str(tuple(count)[0]) + " Total Results for \'" + q + "\'."
        offset = (page-1) * 30

        select_query = 'SELECT channel, text, videos.vid, CAST(timestamp as INTEGER) FROM corpus INNER JOIN videos ON corpus.vid = videos.vid WHERE text LIKE ? LIMIT 30 OFFSET ?;'

        result = cursor.execute(
        select_query,
        ('% '+q+' %', offset,)).fetchall()
        result = [tuple(row) for row in result]
        result.append([count])
        cursor.close()
        return render_template('index.html', results = result, pages = pages, params = q)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    results = [("No results", "0 results returned")]
    if request.method == 'POST':
        print("recieved post from / !")
        query = request.form['query']
        page = 1
        return redirect(url_for("search.search_corpus", q=query, page=page), code=301)

    return render_template('index.html', results = results)