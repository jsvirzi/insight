from datetime import datetime as dt
import sys
from flask import render_template
from flask import request, Response
from app import app
import happybase 
import urllib
import json

# ROUTING/VIEW FUNCTIONS
@app.route('/')
@app.route('/index')
def index():
# Renders index.html.
    return render_template('index.html')

@app.route('/author')
def contact():
# Renders author.html.
    return render_template('author.html')

@app.route('/apidoc')
def apidoc():
# Renders docapi.html.
    return render_template('apidoc.html')

@app.route('/mr1/', methods=['GET'])
def mr1(author):
    connection = happybase.Connection('localhost') 
    table = connection.table('jsvirzi_mr1_hbase') 
    author = author.replace('%20', ' ')
#    try:
    row = table.row('"' + author + '"') 
#    except:
#        row = "mydata"
#        pass
    my_str = row['metadata:field'] 
    my_str = my_str.replace('\\', '')
    n = len(my_str)
    my_str = my_str[1:n-1]
    print my_str
    docs = json.loads(my_str)
    arxiv_ids = docs['arxiv_id']
    n = len(arxiv_ids)
    dates = docs['date']
    n = len(dates)
    print 'length = %d' % n
    # return request.query_string + '<br>' + author + '<br>'

    html = '<!DOCTYPE html>\n\n'
    html += '<html>\n'
    html += '<head><title>mr3</title></head>\n'
    html += '<body>\n'
    html += '<table border="0">\n'
    html += '<tr>\n'
    html += '<th>Document</th>\n'
    html += '<th>Date</th>\n'
    html += '</tr>\n'

    n_rows = 10
    n_cols = (n + 9) / 10

    for i in range(0, n_rows):
        html += '<tr>\n'
        for j in range(0, n_cols):

            k = 10 * j + i

            if k >= n:
                continue

            arxiv_id = arxiv_ids[k]
            date = dates[k]
            print 'arxiv_id %d = %s' % (k, arxiv_id)
            html += '<td>\n'
            html += '<form action="" method="GET">\n'
            html += '<input type="submit" name="arxiv_id" value="' + arxiv_id
            html += '" action="http://ec2-54-183-207-177.us-west-1.compute.amazonaws.com:5000/mr3">\n'
            html += '</form>\n'
            html += '</td>\n'
            html += '<td>\n'
            html += date + '\n'
            html += '</td>\n'
        html += '</tr>\n'

    html += '</table>\n'

    html += '<br>\n'
    html += '<br>\n'

    html += '</body>\n'
    html += '</html>\n'

    return html

@app.route('/mr2/', methods=['GET'])
def mr2(arxiv_id):
    connection = happybase.Connection('localhost') 
    table = connection.table('jsvirzi_mr2a_hbase') 
    arxiv_id = arxiv_id.replace('%20', ' ')
    row = table.row('"' + arxiv_id + '"') 
    my_str = row['metadata:field'] 
    my_str = my_str.replace('\\', '')
    n = len(my_str)
    my_str = my_str[1:n-1]
    print my_str
    docs = json.loads(my_str)
    authors = docs['author']
    abstract = docs['abstract']
    title = docs['title']
    n = len(authors)
    date = docs['date']
    print 'length = %d' % n

    html = '<!DOCTYPE html>\n\n'
    html += '<html>\n'
    html += '<head><title>mr3</title></head>\n'
    html += '<body>\n'
    html += '<table border="0">\n'
    html += '<h1>Title: </h1><p style="font-size:25px">' + title + '</p>\n<br>'
    html += '<h1>Abstract:</h1><p style="font-size:25px">' + abstract + '</p>\n<br>' 
    html += '<tr>\n'
    html += '<th>Document</th>\n'
    html += '<th>Date</th>\n'
    html += '</tr>\n'

    for i in range(0, n):
        author = authors[i]
        print 'arxiv_id %d = %s' % (i, arxiv_id)
        html += '<tr>\n'
        html += '<td>\n'
        html += '<form action="" method="GET">\n'
        html += '<input type="submit" name="author" value="' + author
        html += '" action="http://ec2-54-183-207-177.us-west-1.compute.amazonaws.com:5000/mr3">\n'
        html += '</form>\n'
        html += '</td>\n'
        html += '<td>\n'
        html += '</td>\n'
        html += '</tr>\n'

    html += '</table>\n'

    html += '<br>\n'
    html += '<br>\n'
    html += '<br>\n'
    html += '<form action="" method="GET">\n'
    html += '</form>\n'

    html += '</body>\n'
    html += '</html>\n'

    return html

@app.route('/mr3/', methods=['GET'])
def mr3(author):

    colors = ['orange', 'blue', 'red', 'purple', 'magenta', 'green', 'yellow', 'cyan']

    connection = happybase.Connection('localhost') 
    table = connection.table('jsvirzi_mr3_hbase') 
    # author = request.args.get("author")
    author = author.replace('%20', ' ')
#    try:
    row = table.row('"' + author + '"') 
#    except:
#        row = "mydata"
#        pass
    my_str = row['metadata:field'] 
    my_str = my_str.replace('\\', '')
    n = len(my_str)
    my_str = my_str[1:n-1]
    # print my_str
    docs = json.loads(my_str)
    collaborators = docs['collaborators']
    n = len(collaborators)
    # print 'length = %d' % n
    frequencies = []
    frequencies_str = docs['frequency']
    for my_str in frequencies_str:
        frequencies.append(int(my_str))
    n = len(frequencies)
    # print 'length = %d' % n
    # return request.query_string + '<br>' + author + '<br>'

    n_rows = 10
    n_cols = (n + 9) / 10

    html = '<!DOCTYPE html>\n\n'
    html += '<html>\n'
    # html += '<head><link rel="stylesheet" type="text/css" href="insight.css"><title>mr3</title></head>\n'
    html += '<head>\n'
    html += '<style> #xxx td { text-align: center; color:"#dddddd"; } </style><title>XXX</title>\n'

    html += '<script type="text/javascript" src="http://jsvirzi.dyndns.org/~jsvirzi/insight/canvasjs.min.js"></script>\n'
    html += '<script type="text/javascript">\n'
    html += 'window.onload = function () {\n'
    html += 'var chart = new CanvasJS.Chart("chartContainer",\n'
    html += '{ title:{text:"Collaborators for ' + author + '"},\n'
    html += 'data: [ { type: "column", dataPoints: [\n'

    x_axis = []
    y_axis = []
    n = len(collaborators)
    for i in range(0, n):
        if frequencies[i] <= 1:
            continue
        x_axis.append(collaborators[i])
        y_axis.append(str(frequencies[i]))

    n = len(x_axis)
    j = 0
    k = len(colors)
    for i in range(0, n):
        y_value = y_axis[i]
        x_label = x_axis[i]
        my_color = colors[j]
        j = j + 1
        if j >= k:
            j = 0
        html += '{ x: ' + str(i) + ', y : ' + y_value + ', label:"' + x_label + '", color: "' + my_color + '"},\n' 
    html += ']}\n'
    html += ']\n'
    html += '});\n'
     
    html += 'chart.render();\n'
    html += '}\n'
    html += '</script>\n'
    html += '</head>\n'

    html += '<body>\n'
    html += '<h1>Collaborators for ' + author + '</h1><br>\n'
    html += '<div id="chartContainer" style="height: 250px; width: 80%;"></div>\n'

#    html += '</body>\n'
#    html += '</html>\n'

#    print html

#    return html

    html += '<table border="0" id="xxx">\n'
    html += '<tr>\n'
    for i in range(0, n_cols):
        html += '<th>Collaborator</th>\n'
        html += '<th>Frequency</th>\n'
    html += '</tr>\n'

    col2 = collaborators
    fre2 = frequencies 
    points = zip(fre2, col2)
    sorted_points = sorted(points, reverse = True)
    frequencies = [point[0] for point in sorted_points]
    collaborators = [point[1] for point in sorted_points]

    for i in range(0, n_rows):
        html += '<tr>\n'
        for j in range(0, n_cols):

            k = 10 * j + i
            if k >= n:
                continue
            collaborator = collaborators[k]
            frequency = frequencies[k]

            # print 'collaborator %d = %s %s' % (k, collaborator, frequency)

            html += '<td>\n'
            html += '<form action="" method="GET">\n'
            html += '<input type="submit" name="author" value="' + collaborator
            html += '" action="http://ec2-54-183-207-177.us-west-1.compute.amazonaws.com:5000/mr3">\n'
            html += '</form>\n'
            html += '</td>\n'
            html += '<td bordercolor="#dddddd">' + str(frequency) + '</td>'
            html += '</td>\n'
    
        html += '</tr>\n'

    html += '</table>\n'

    html += '<br>\n'
    html += '<br>\n'
    html += '<br>\n'
    html += '<form action="" method="GET">\n'
    html += '</form>\n'

    html += '</body>\n'
    html += '</html>\n'

    return html

@app.route('/mr6/', methods=['GET'])
def mr6(author):

    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    colors = ['orange', 'blue', 'red', 'purple', 'magenta', 'green', 'yellow', 'cyan']

    connection = happybase.Connection('localhost') 
    table = connection.table('jsvirzi_mr6_hbase') 
    # author = request.args.get("author")
    author = author.replace('%20', ' ')
    row = table.row('"' + author + '"') 
    json_string = row['metadata:field'] 

    json_string = json_string.replace('\\', '')
    n = len(json_string)
    json_string = json_string[1:n-1]
    # print 'JSON STRING = ' + json_string

    docs = json.loads(json_string)

    dates = docs['citation_dates']

    min_date = 999999
    max_date = 0
    for date in dates:
	    my_list = date.split('-')
	    year = int(my_list[0])
	    month = int(my_list[1])

	    a = year * 100 + month

	    if a > max_date:
		    max_date = a

	    if a < min_date:
		    min_date = a

    max_string = str(max_date)
    min_string = str(min_date)

    max_year = int(max_string[0:4])
    min_year = int(min_string[0:4])

    max_month = int(max_string[4:6])
    min_month = int(min_string[4:6])

    year = min_year
    month = min_month - 1

    axis_list = []

    while month < 12:
	    my_str = months[month] + '-' + str(year)
	    axis_list.append(my_str)
	    month = month + 1

    year = year + 1
 
    while year < max_year:
	    for month in range(0, 12):
		    my_str = months[month] + '-' + str(year)
		    axis_list.append(my_str)
	    year = year + 1

    year = max_year
    for month in range(0, max_month):
	    my_str = months[month] + '-' + str(year)
	    axis_list.append(my_str)

    date_data = []
    for q in dates:
	    my_list = q.split('-')
	    year_str = my_list[0]
	    month_str = my_list[1]
	    i = int(month_str)
	    my_str = months[i-1] + '-' + year_str
	    date_data.append(my_str)

    counts = []
    for p in axis_list:
	    n = date_data.count(p)
	    counts.append(n)

    html = '<!DOCTYPE HTML>\n\n'
    html += '<html>\n'
    html += '<head>\n'
    html += '<script type="text/javascript" src="http://jsvirzi.dyndns.org/~jsvirzi/insight/canvasjs.min.js"></script>\n'
    html += '<script type="text/javascript">\n'
    html += 'window.onload = function () {\n'
    html += 'var chart = new CanvasJS.Chart("chartContainer",\n'
    html += '{ title:{text:"Citation History for ' + author + '"},\n'
    html += 'data: [ { type: "column", dataPoints: [\n'
    n = len(axis_list)
    j = 0
    k = len(colors)
    for i in range(0, n):
        date = axis_list[i]
        my_color = colors[j]
        my_color = 'red'
        j = j + 1
        if j >= k:
            j = 0
        html += '{ x: ' + str(i) + ', y : ' + str(counts[i]) + ', label:"' + date + '", color: "' + my_color + '"},\n' 
    html += ']}\n'
    html += ']\n'
    html += '});\n'
     
    html += 'chart.render();\n'
    html += '}\n'
    html += '</script>\n'
    html += '</head>\n'

    html += '<body>\n'
    html += '<div id="chartContainer" style="height: 250px; width: 80%;"></div>\n'
    html += '</body>\n'
    html += '</html>\n'

    # print html

    return html

@app.route('/mrX/', methods=['GET'])
def mrX():
    author = request.args.get("author")
    arxiv_id = request.args.get("arxiv_id")
    query = request.args.get("query")

    print 'arxiv id = %s. author = %s' % (arxiv_id, author)

    if query == 'citations':
        return mr6(author)
    elif query == 'collaborators':
        return mr3(author)
    elif query == 'submissions':
        return mr1(author)
    elif query == 'authors':
        return mr2(arxiv_id)

# @app.route('/api/gdelt/event/<int:globaleventid>', methods=['GET'])
# def api():
# Queries the DB and returns data
# cur = db.cursor()   
    # return render_template('api.html')

# @app.route('/api/top', methods=['GET'])
# def api():
# Queries the DB and returns data
# cur = db.cursor()   
    # return render_template('api.html')
