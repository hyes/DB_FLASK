from flask import Flask, request, render_template, flash, url_for, redirect
from flaskext.mysql import MySQL
import json


app = Flask(__name__)
mysql = MySQL();

app.secret_key = 'some_secret'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'db1004'
app.config['MYSQL_DATABASE_DB'] = 'dbnews'

mysql.init_app(app)

@app.route('/')
def hello_world():
	return 'Hello World!!'

@app.route('/loadData', methods = ["GET","POST"])
def loadData():
	cursor = mysql.connect().cursor()
	cursor.execute("select * from mainnews")

	result = []
	column = tuple( [d[0] for d in cursor.description] )

	for row in cursor:
		result.append(dict(zip(column, row)))
		print(result)

	return json.dumps(result)

@app.route('/load/', methods = ["GET","POST"])
def load():
	cursor = mysql.connect().cursor()
	cursor.execute("select ArticleNumber, Title, Content from mainnews")
	
	temp = cursor.fetchall()
	entries = (list(temp))
	
	return render_template('test.html', entries = entries)


@app.route('/add', methods = ["POST"])
def upload():
	if request.method == "POST":

		Content = request.form['Content']
		#Writer = request.form['Writer']
		#WriteDate = request.form['WriteDate']
		Title = request.form['Title']
		
		con = mysql.connect()
		cursor = con.cursor()

		query = "insert into mainnews \
		(Title, Content) values \
		('" + Title + "','" + Content + "');"
		cursor.execute(query)
		con.commit()
		flash("successfully saved")
		return redirect(url_for('load'))

@app.route("/load/<no>", methods = ["GET","POST"])
def showDetail(no):
	cursor = mysql.connect().cursor()
	q1 = "select ArticleNumber, Title, Content from mainnews \
		where ArticleNumber = "
	q2 = no
	query = q1 + q2
	print(query)
	cursor.execute(query)

	temp = cursor.fetchall()
	entries = (list(temp))

	reply_q = "select Title, Content from reply where ArticleNumber = "
	reply_query = reply_q + q2

	cursor.execute(reply_query)
	temp2 = cursor.fetchall()
	replies = (list(temp2))

	return render_template('showDetail.html', entries = entries, replies = replies)

@app.route("/load/re/<no>", methods = ["POST"])
def reply(no):
	if request.method == "POST":
		ArticleNumber = no
		Content = request.form['Content']
		Title = request.form['Title']
		
		con = mysql.connect()
		cursor = con.cursor()

		query = "insert into reply \
		(Title, Content, ArticleNumber) values \
		('" + Title + "','" + Content + "','" + ArticleNumber + "');"

		cursor.execute(query)
		con.commit()
		flash("successfully saved")
		return redirect(url_for('showDetail', no = no))


@app.errorhandler(404)
def not_found(error):
	return ("404error!!")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 8000, debug = True)