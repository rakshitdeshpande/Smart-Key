import pymongo
from flask import Flask, render_template, url_for, redirect, request ,flash ,session
from pymongo import MongoClient

app = Flask(__name__)

global user

@app.route('/')
def index():
	return render_template('index.html')

@app.errorhandler(404)
def notFound(e):
    return render_template("404.html"), 404

@app.route('/user_login', methods=['POST','GET'])
def user_login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method == "POST":
        print("POST came")
        file = open("password","r")
        string = file.read()
        client = pymongo.MongoClient(string)
        db = client.test
        x = db.test_collection.find({"name":request.form["username"]})
        # print(x[0]["password"])
        if x[0]["password"] == request.form["password"]:
            print("HELLO")
            session['user'] = request.form["username"]
            return redirect("/skmanager")
        else:
            return redirect("/user_login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/user_login")

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
         name = request.form['name']
         email = request.form['email']
         gender = request.form['gender']
         DLNo = request.form['DLNo']
         dob = request.form['dob']
         blood_group = request.form['Blood Group']
         valid_till = request.form['valid_till']
         password = request.form['password']
         file = open("password","r")
         string = file.read()
         client = pymongo.MongoClient(string)
         db = client.test
         cred = {"name":name,"email":email,"gender":gender,"DLNo":DLNo,"dob":dob,"blood_group":blood_group,"valid_till":valid_till,"password":password}
         db.test_collection.insert(cred)
         return redirect("/skmanager")
    else:
        return render_template("/signup.html")

    

@app.route('/skmanager',methods=["POST","GET"])
def skmanager():
    if request.method == 'GET':
        file = open("password","r")
        string = file.read()
        client = pymongo.MongoClient(string)
        db = client.test
        data = db.test_collection.find({"name":session[user]})
        return render_template('sk_manager.html',data = data)

@app.route('/delete')
def delete():
    file = open("password","r")
    string = file.read()
    client = pymongo.MongoClient(string)
    db = client.test
    db.test_collection.delete_many({})
    return render_template("sucess.html")

@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
    if request.method == 'GET':
        file = open("password","r")
        string = file.read()
        client = pymongo.MongoClient(string)
        db = client.test
        data = db.test_collection.find({},{"_id":0})
        return render_template('dashboard.html',data = data)

@app.route('/sample')
def sample():
    return render_template("sample.html")

@app.route('/session')
def session():
    return render_template("session.html")

    
@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        session['name'] = request.form('name')
        return redirect(url_for('index'))
    return render_template("session.html")

# @app.route('/index')
# def index():
#     if 'name' in session:
#         #user = session['name']
#         return "Succesfully logged in"
#     return "You are not logged in"

# @app.route('/logout')
# def logout():
#     session.pop('name,None')
#     print("logged out")
#     return redirect('/login')

@app.route('/code',methods=['GET','POST'])
def code():
    if request.method == 'POST':
        codeDetails = request.form
        code = codeDetails['code']
        file = open("password","r")
        string = file.read()
        client = pymongo.MongoClient(string)
        db = client.test
        
    

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, threaded = True, debug = True)
    # app.run(debug=True)
