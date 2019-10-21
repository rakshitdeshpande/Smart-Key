import pymongo
from flask import Flask, render_template, url_for, redirect, request ,flash ,session
from pymongo import MongoClient

app = Flask(__name__)

app.secret_key = 'Smart-Key'

file = open("password","r")
string = file.read()
client = pymongo.MongoClient(string)
db = client.test

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/user_login', methods=['POST','GET'])
def user_login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method == "POST" :
        if (request.form["name"] == "admin" and request.form["password"] == "admin"):
            session['username'] = request.form["name"]
            return redirect('/dashboard')
        x = db.test_collection.find({"name":request.form["name"]})
        if(x[0]["password"] == request.form["password"]):
            session['username'] = request.form['name']
            return redirect(url_for("skmanager"))
        else:
            return redirect("/user_login")

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
         insuranceNo  request.form['insuranceNo']
         insurance_valid_till = request.form['insurance_valid_till']
         password = request.form['password']
         rfid = request.form['rfid']
         cred = {"name":name,"email":email,"gender":gender,"dob":dob,"blood_group":blood_group,"DLNo":DLNo,"dl_valid_till":dl_valid_till,"insuranceNo":insuranceNo,"insurance_valid_till":insurance_valid_till"password":password,"code":rfid}
         db.test_collection.insert(cred)
         session['username'] = request.form['name']
         return redirect(url_for("skmanager"))
    else:
        return render_template("/signup.html")

@app.route('/skmanager',methods=["POST","GET"])
def skmanager():
    if request.method == 'GET':
        if 'username' in session:
            user = session['username']
            data = db.test_collection.find({"name":user})
            return render_template('sk_manager.html',data = data)
        return "You are not logged in <br><a href = '/user_login'></b>" + "click here to log in</b></a>"

@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
    if request.method == 'GET':
        if 'username' in session and session['username'] == "admin":
            data = db.test_collection.find({},{"_id":0})
            return render_template('dashboard.html',data = data)
        return "You are not logged in <br><a href = '/user_login'></b>" + "click here to log in</b></a>"

@app.route('/code',methods=['GET','POST'])
def code():
    if request.method == 'POST':
            codeDetails = request.form['code']
            x = db.test_collection.find()
            if x[0]["code"] == codeDetails :
                return "true"
            else:
                return "false"

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("index"))

@app.errorhandler(404)
def notFound(e):
    return render_template("404.html"), 404
    return redirect(url_for("index"))      

@app.route('/delete')
def delete():
    db.test_collection.delete_many({})
    return render_template("sucess.html")

@app.route('/fetch')
def fetch():
    data = db.test_collection.find()
    return render_template("fetch.html",data = data)

@app.route('/sample')
def sample():
    return render_template("sample.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, threaded = True, debug = True)
    

    
