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

import sqlite3
import re

def match(expr, item):
    reg = re.compile(expr, re.I)
    return reg.search(item) is not None

@login_required
@bp.route('/search/<string:q>/<int:page>', methods=['GET', 'POST'])
def search_corpus(q, page):
    # print(request.args.get('string:q'))
    if request.method == 'GET':
        pos = ".*" # the pos regex query
        q = q.strip()
        q_unchanged = q
        if match(r'(\<[A-Z]{1,4}\>)|(\<\.\>)', q):
            # Method: 2 pass regex filtering (Query + POS)
            # q = Hello \w+ my name is \w+
            # pos = \w+ PRON \w+ \w+ NOUN
            all_pos = ['NOUN','PRON','ADJ','VERB','ADV','ADP','PRT','DET','CONJ','NUM']
            print("GRAMMAR SEARCH:")
            print(f"plain q: {q}")
            # pos_exp = re.findall(r'\<(.*?)\>', q)
            q_tmp = re.findall(r'[a-zA-Z0-9]+', q)
            pos = []
            print(q)
            for i,v in enumerate(q_tmp):
                if v in all_pos:
                    q_tmp[i] = "[a-zA-Z0-9]+"
                    pos.append(v)
                else:
                    pos.append("[A-Z.]+")
            q = " ".join(q_tmp)
            pos = " ".join(pos)
            # print(f'q = {q}')
            # print(f'pos = {pos}')

        cursor = get_db()
        cursor.create_function("REGEXP", 2, match)
        select_query = 'SELECT COUNT(*) FROM corpus WHERE text REGEXP ? AND pos REGEXP ?;'

        count = cursor.execute(
        select_query,
        (q,pos)).fetchone()
        total_pages = int(math.ceil(int(tuple(count)[0]) / 30 + 0.01))
        pages = list(range(1, total_pages+1))

        count = str(tuple(count)[0]) + " Total Results for \'" + q_unchanged + "\'."
        offset = (page-1) * 30

        select_query = 'SELECT channel, text, videos.vid, CAST(timestamp as INTEGER) FROM corpus INNER JOIN videos ON corpus.vid = videos.vid WHERE text REGEXP ? AND pos REGEXP ? LIMIT 30 OFFSET ?;'

        result = cursor.execute(
        select_query,
        # ('% '+q+' %', offset,)).fetchall()
        (q, pos, offset,)).fetchall()
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
        return redirect(url_for("search.search_corpus", q=q, page=page), code=301)
        # cursor = get_db()
        # cursor.create_function("REGEXP", 2, match)
        # select_query = 'SELECT COUNT(*) FROM corpus WHERE text REGEXP ?;'
        # count = cursor.execute(
        # select_query,
        # # ('% '+q+' %',)).fetchone()
        # (q,)).fetchone()
        # total_pages = int(math.ceil(int(tuple(count)[0]) / 30 + 0.01))
        # pages = list(range(1, total_pages+1))

        # count = str(tuple(count)[0]) + " Total Results for \'" + q + "\'."
        # offset = (page-1) * 30

        # select_query = 'SELECT channel, text, videos.vid, CAST(timestamp as INTEGER) FROM corpus INNER JOIN videos ON corpus.vid = videos.vid WHERE text REGEXP ? LIMIT 30 OFFSET ?;'

        # result = cursor.execute(
        # select_query,
        # # ('% '+q+' %', offset,)).fetchall()
        # (q, offset,)).fetchall()
        # result = [tuple(row) for row in result]
        # result.append([count])
        # cursor.close()
        # return render_template('index.html', results = result, pages = pages, params = q)

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