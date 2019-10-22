import pymongo,datetime
from flask import Flask, render_template, url_for, redirect, request ,flash ,session
from pymongo import MongoClient
from flask_mail import Mail,Message

app = Flask(__name__)

app.secret_key = 'Smart-Key'

file = open("password","r")
string = file.read()
client = pymongo.MongoClient(string)
db = client.test

file = open("id","r")
id = file.read()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rakshitdeshpande375@gmail.com'
app.config['MAIL_PASSWORD'] = id
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def user_login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method == "POST" :
        try:
            if (request.form["name"] == "admin" and request.form["password"] == "admin"):
                session['username'] = request.form["name"]
                return redirect('/dashboard')
            x = db.details.find({"name":request.form["name"]})
            if(x[0]["password"] == request.form["password"]):
                session['username'] = request.form['name']
                email_id = x[0]["email"]
                msg = Message('RTO', sender = 'rakshitdeshpande375@gmail.com', recipients = [email_id])
                msg.body = "You have successfully logged in"
                mail.send(msg)
                return redirect(url_for("skmanager"))
            else:
                return redirect("/login")
        except:
            return render_template('/login')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
         name = request.form['name']
         email = request.form['email']
         gender = request.form['gender']
         dob = request.form['dob']
         blood_group = request.form['Blood Group']
         DLNo = request.form['DLNo']
         dl_valid_till = request.form['dl_valid_till']
         insuranceNo  = request.form['insuranceNo']
         insurance_valid_till = request.form['insurance_valid_till']
         password = request.form['password']
         rfid = request.form['rfid']
         cred = {"name":name,"email":email,"gender":gender,"dob":dob,"blood_group":blood_group,"DLNo":DLNo,"dl_valid_till":dl_valid_till,"insuranceNo":insuranceNo,"insurance_valid_till":insurance_valid_till,"password":password,"code":rfid}
         db.details.insert(cred)
         session['username'] = request.form['name']
         msg = Message('RTO', sender = 'rakshitdeshpande375@gmail.com', recipients = [email])
         msg.body = "You have successfully signed in"
         mail.send(msg)
         return redirect(url_for("skmanager"))
    else:
        return render_template("/signup.html")

@app.route('/skmanager',methods=["POST","GET"])
def skmanager():
    if request.method == 'GET':
        if 'username' in session:
            user = session['username']
            data = db.details.find({"name":user})
            logs = db.logs.find({"name":user})
            return render_template('sk_manager.html',data = data,logs = logs)
        return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"

@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
    if request.method == 'GET':
        if 'username' in session and session['username'] == "admin":
            data = db.details.find({},{"_id":0})
            user = session['username']
            logs = db.logs.find({"name":user})
            return render_template('dashboard.html',data = data,logs = logs)
        return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"

@app.route('/code',methods=['GET','POST'])
def code():
    if request.method == 'POST':
            codeDetails = request.form['code']
            x = db.details.find()
            if x[0]["code"] == codeDetails :
                return "true"
            else:
                return "false"

@app.route("/logout")
def logout():
    try:
        name = session['username']
        a = datetime.datetime.now()
        time = a.strftime("%c")
        log = {"name":name,"time":time}
        db.logs.insert(log)
        session.pop('username', None)
        return redirect(url_for("index"))
    except:
        return redirect(url_for("index"))

@app.errorhandler(404)
def notFound(e):
    return render_template("404.html"), 404
    return redirect(url_for("index"))      

@app.route('/delete')
def delete():
    db.details.delete_many({})
    # db.logs.delete_many({})
    return render_template("sucess.html")

@app.route('/clear_log')
def clear_log():
    db.logs.delete_many({})
    return render_template("sucess.html")

@app.route('/fetch')
def fetch():
    data = db.details.find()
    return render_template("fetch.html",data = data)

@app.route('/sample')
def sample():
    return render_template("sample.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, threaded = True, debug = True)