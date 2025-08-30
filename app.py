import sqlite3

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


database = r'my_database.db'


def get_db():
    conn = sqlite3.connect(database)
    return conn


def group_by_index(data, index, sort_key=None):
    grouped_data = {}
    for item in data:
        key = item[index]
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(item)
    for key in grouped_data:
        grouped_data[key] = sorted(grouped_data[key], key=sort_key)
    three_dim_list = list(grouped_data.values())
    three_dim_list.sort(key=lambda x: x[0][index])
    return three_dim_list


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dictionary/<letter>')
def dictionary(letter):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM 第一轮标注记录 WHERE 音序 =?',(letter,))
    data_raw = cursor.fetchall()
    data = group_by_index(data_raw,12,lambda x:x[2])
    return render_template('entry_list.html',letter=letter,data=data)


@app.route('/predicate/<pr>')
def predicate_detail(pr):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM 第一轮标注记录 WHERE 述语词例 = ?',(pr,))
    predicate_info = cursor.fetchall()
    predicate_info = [[item if item != "na" else "" for item in row] for row in predicate_info]
    predicate_info = group_by_index(predicate_info,16,lambda x:x[2])
    return render_template('predicate_detail.html',predicate_info=predicate_info,pr=pr)


@app.route('/complement/<com>')
def complement_detail(com):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM 第一轮标注记录 WHERE 补语词例 = ?',(com,))
    complement_info = cursor.fetchall()
    complement_info= [[item if item != "na" else "" for item in row] for row in complement_info]
    complement_info = group_by_index(complement_info,28,lambda x:x[2])
    return render_template('complement_detail.html', complement_info=complement_info, com=com)


@app.route('/vrc/<vr>')
def vrc_detail(vr):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM 第一轮标注记录 WHERE 述结式词例 LIKE ?',('%' + vr + '%',))
    vrc_info = cursor.fetchall()
    vrc_info = [[item if item != "na" else "" for item in row] for row in vrc_info]
    vrc_info.sort(key=lambda x:x[2])
    return render_template('vrc_detail.html', vrc_info=vrc_info, vr=vr)


@app.route('/search')
def search():
    search_term = request.args.get('search_term', '')
    search_type = request.args.get('search_type', '')
    if search_type == '按述语搜索':
        return redirect(url_for('predicate_detail', pr=search_term))
    elif search_type == '按补语搜索':
        return redirect(url_for('complement_detail',com=search_term))
    else:
        return redirect(url_for('vrc_detail',vr=search_term))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5005)