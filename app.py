'''
Nokia IOT Smart-Key
'''
import pymongo,datetime,hashlib
from flask import Flask, render_template, url_for, redirect, request ,flash ,session
from pymongo import MongoClient
from flask_mail import Mail,Message
import os

app = Flask(__name__)

app.secret_key = 'Smart-Key'

#accesing environment variables
admin_name = os.environ['ADMIN_NAME']
admin_pass = os.environ['ADMIN_PASS']
db_username = os.environ['DB_USERNAME']
db_pass = os.environ['DB_PASS']
db = client.test
id = os.environ['MAIL_PASS']
mail_id = os.environ['MAIL_ID']

#connecting to database(mongodb)
client = pymongo.MongoClient("mongodb+srv://"+db_username+":"+db_pass+"@cluster0-qv6wg.mongodb.net/admin?retryWrites=true&w=majority")

#mail-parameters
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mail_id
app.config['MAIL_PASSWORD'] = id
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
         name = request.form['name']
         email = request.form['email']
         phone = request.form['phone_number']
         gender = request.form['gender']
         dob = request.form['dob']
         blood_group = request.form['Blood Group']
         DLNo = request.form['DLNo']
         dl_valid_till = request.form['dl_valid_till']
         insuranceNo  = request.form['insuranceNo']
         insurance_valid_till = request.form['insurance_valid_till']
         password = request.form['password']
         rfid = request.form['rfid']
         if name == "" or email == "" or gender == "" or dob == "" or blood_group == "" or DLNo == "" or dl_valid_till == ""or insuranceNo == ""or insurance_valid_till == ""or password == ""or rfid == "":
             return redirect('/signup')
         pass_256 = hashlib.sha256(password.encode())  #sha256 encryption
         pass_encrpt = pass_256.hexdigest()
         cred = {"name":name,"email":email,"phone_number":phone,"gender":gender,"dob":dob,"blood_group":blood_group,"DLNo":DLNo,"dl_valid_till":dl_valid_till,"insuranceNo":insuranceNo,"insurance_valid_till":insurance_valid_till,"password":pass_encrpt,"code":rfid,"ignition_status":"off","dl_validity":"","insurance_validity":""}
         db.details.insert(cred)
         session['username'] = request.form['name']
         y = datetime.datetime.now()
         date = y.strftime("%d")
         month = y.strftime("%m")
         year = y.strftime("%Y")
         
         x = db.details.find({"name":name})
         z = x[0]["dl_valid_till"]
         valid = z.split("-")
         if valid[0]>year:
             db.details.update({"name":name},{"$set":{"dl_validity":"Valid"}})
         elif valid[0]>=year and valid[1]>month:
	         db.details.update({"name":name},{"$set":{"dl_validity":"Valid"}})
         elif valid[0]>=year and valid[1]>=month and valid[2]>=date :
	         db.details.update({"name":name},{"$set":{"dl_validity":"Valid"}})
         else:
             db.details.update({"name":name},{"$set":{"dl_validity":"In Valid"}})
             msg = Message('DL Expired', sender = mail_id, recipients = [email])
             msg.body = "Dear customer your Driving License has been expired, please renew it as early as possible"
             mail.send(msg)
         
         z = x[0]["insurance_valid_till"]
         valid = z.split("-")
         if valid[0]>year:
	         db.details.update({"name":name},{"$set":{"insurance_validity":"Valid"}})
         elif valid[0]>=year and valid[1]>month:
	         db.details.update({"name":name},{"$set":{"insurance_validity":"Valid"}})
         elif valid[0]>=year and valid[1]>=month and valid[2]>=date :
             db.details.update({"name":name},{"$set":{"insurance_validity":"Valid"}})
         else:
             db.details.update({"name":name},{"$set":{"insurance_validity":"In Valid"}})
             msg = Message('Insurance Expired', sender = mail_id, recipients = [email])
             msg.body = "Dear customer your Insurance has been expired, please renew it as early as possible"
             mail.send(msg)
    
         msg = Message('RTO', sender = mail_id, recipients = [email])
         msg.body = "You have successfully signed in"
         mail.send(msg)
         return redirect(url_for("skmanager"))
    else:
        return render_template("/signup.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method == "POST" :
        try:
            if (request.form["name"] == admin_name and request.form["password"] == admin_pass):
                session['username'] = request.form["name"]
                return redirect('/dashboard')
            x = db.details.find({"name":request.form["name"]})
            password = request.form["password"]
            pass_256 = hashlib.sha256(password.encode())
            pass_encrypt = pass_256.hexdigest()
            if(x[0]["password"] == pass_encrypt):
                session['username'] = request.form['name']
                name = session['username']
                y = datetime.datetime.now()
                date = y.strftime("%d")
                month = y.strftime("%m")
                year = y.strftime("%Y")
                email = x[0]["email"]
                z = x[0]["dl_valid_till"]
                valid = z.split("-")
                if valid[0]>year:
	                db.details.update({"name":name},{"$set":{"dl_validity":"Valid"}})
                elif valid[0]>=year and valid[1]>month:
	                db.details.update({"name":name},{"$set":{"dl_validity":"Valid"}})
                elif valid[0]>=year and valid[1]>=month and valid[2]>=date :
	                db.details.update({"name":name},{"$set":{"dl_validity":"Valid"}})
                else:
                    db.details.update({"name":name},{"$set":{"dl_validity":"In Valid"}})
                    msg = Message('DL Expired', sender = mail_id, recipients = [email])
                    msg.body = "Dear customer your Driving License has been expired, please renew it as early as possible"
                    mail.send(msg)
                
                z = x[0]["insurance_valid_till"]
                valid = z.split("-")
                if valid[0]>year:
	                db.details.update({"name":name},{"$set":{"insurance_validity":"Valid"}})
                elif valid[0]>=year and valid[1]>month:
	                db.details.update({"name":name},{"$set":{"insurance_validity":"Valid"}})
                elif valid[0]>=year and valid[1]>=month and valid[2]>=date :
	                db.details.update({"name":name},{"$set":{"insurance_validity":"Valid"}})
                else:
                    db.details.update({"name":name},{"$set":{"insurance_validity":"In Valid"}})
                    msg = Message('Insurance Expired', sender = mail_id, recipients = [email])
                    msg.body = "Dear customer your Insurance has been expired, please renew it as early as possible"
                    mail.send(msg)

                msg = Message('RTO', sender = mail_id, recipients = [email])
                msg.body = "You have successfully logged in"
                mail.send(msg)
                return redirect(url_for("skmanager"))
            else:
                return redirect("/login")
        except:
            return redirect('/login')

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

#update the users details
@app.route('/update',methods=['GET','POST'])
def update():
    if 'username' in session:
        try:
            if request.method == 'GET':
                return render_template("update.html")
            else:
                email = request.form['email']
                phone = request.form['phone_number']
                dl_valid_till = request.form['dl_valid_till']
                insurance_valid_till = request.form['insurance_valid_till']
                password = request.form['password']
                user = session['username']
                if email != "":
                    db.details.update({"name":user},{"$set":{"email":email}})
                if phone != "":
                    db.details.update({"name":user},{"$set":{"phone_number":phone}})
                if dl_valid_till != "":
                    db.details.update({"name":user},{"$set":{"dl_valid_till":dl_valid_till}})
                if insurance_valid_till != "":
                    db.details.update({"name":user},{"$set":{"insurance_valid_till":insurance_valid_till}})
                if password != "":
                    db.details.update({"name":user},{"$set":{"password":password}})

                y = datetime.datetime.now()
                date = y.strftime("%d")
                month = y.strftime("%m")
                year = y.strftime("%Y")
            
                x = db.details.find({"name":user})
                email = x[0]["email"]
                z = x[0]["dl_valid_till"]
                valid = z.split("-")
                if valid[0]>year:
	                db.details.update({"name":user},{"$set":{"dl_validity":"Valid"}})
                elif valid[0]>=year and valid[1]>month:
	                db.details.update({"name":user},{"$set":{"dl_validity":"Valid"}})
                elif valid[0]>=year and valid[1]>=month and valid[2]>=date :
	                db.details.update({"name":user},{"$set":{"dl_validity":"Valid"}})
                else:
                    db.details.update({"name":user},{"$set":{"dl_validity":"In Valid"}})
                    msg = Message('DL Expired', sender = mail_id, recipients = [email])
                    msg.body = "Dear customer your Driving License has been expired, please renew it as early as possible"
                    mail.send(msg)
                
                z = x[0]["insurance_valid_till"]
                valid = z.split("-")
                if valid[0]>year:
	                db.details.update({"name":user},{"$set":{"insurance_validity":"Valid"}})
                elif valid[0]>=year and valid[1]>month:
	                db.details.update({"name":user},{"$set":{"insurance_validity":"Valid"}})
                elif valid[0]>=year and valid[1]>=month and valid[2]>=date :
	                db.details.update({"name":user},{"$set":{"insurance_validity":"Valid"}})
                else:
                    db.details.update({"name":user},{"$set":{"insurance_validity":"In Valid"}})
                    msg = Message('Insurance Expired', sender = mail_id, recipients = [email])
                    msg.body = "Dear customer your Insurance has been expired, please renew it as early as possible"
                    mail.send(msg)
            
                msg = Message('Details Updated', sender = mail_id, recipients = [email])
                msg.body = "Dear customer your details has been successfully updated"
                mail.send(msg)
                return redirect('/skmanager')
        except:
            return redirect('/update')
    else:
        return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"

#hardware
@app.route('/code',methods=['GET','POST'])
def code():
    if request.method == 'POST':
            codeDetails = request.form['code']
            try:
                x = db.details.find({"code":codeDetails})
                name = x[0]["name"]
                session['username'] = name
                return "true"
            except:
                return "false"

#updating ignition status 
@app.route('/status',methods = ['GET','POST'])
def status():
    if 'username' in session:
        if request.method == "POST":
            status = request.form["status"]
            name = session['username']
            if status == "1":
                db.details.update({"name":name},{"$set":{"ignition_status":"on"}})
                a = datetime.datetime.now()
                time = a.strftime("%c")
                log = {"name":request.form["name"],"start":time,"stop":"-"}
                db.logs.insert(log)
            else:
                db.details.update({"name":name},{"$set":{"ignition_status":"off"}})
                a = datetime.datetime.now()
                time = a.strftime("%c")
                db.logs.update({"name":name,"start":"-"},{"$set":{"stop":time}})
            return render_template("skmanager.html")
    else:
        return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"
        
@app.route("/logout")
def logout():
    try:
        name = session['username']
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
    if 'username' in session and session['username'] == admin_name:
        db.details.delete_many({})
        # db.logs.delete_many({})
        return render_template("index.html")
    else:
        return render_template("index.html")

@app.route('/clear_log')
def clear_log():
    if 'username' in session and session['username'] == admin_name:
        db.logs.delete_many({})
        return render_template("index.html")
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, threaded = True, debug = True)