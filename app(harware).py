from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml
from flask import redirect, url_for

app = Flask(__name__)

#configuring database
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app) #mysql object(instantiating)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		codeDetails = request.form
		code = codeDetails['code']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO code(bcode) VALUES(%s)", (code,))
		mysql.connection.commit()
		cur.close()
		return "<h1>success</h1>"
		return redirect(url_for('index'))
	else:
		return render_template('index.html')

@app.route('/code', methods=['POST', 'GET'])
def code():
	if request.method == 'POST':
		codeDetails = request.form
		code = codeDetails['code']
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM code WHERE bcode=%s",(code,))
		data = "error" 
		for i in cur:
			data = i
		if data == 'error':
			return "false"
		else:
			return "true"


@app.route('/view', methods=['POST', 'GET'])
def view():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM code")
	data = cur.fetchall()
	return render_template("table.html", value=data)



if __name__ == '__main__':
	app.run(debug=True)