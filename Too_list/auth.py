from flask import Blueprint,render_template,url_for,request,redirect,flash,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
from flask_bcrypt import Bcrypt
from Mongodb import *
from bson import ObjectId
auth = Blueprint("auth",__name__)

@auth.route("/signup")
def signup():
    return  render_template("signup.html")

@auth.route("/signup",methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = collection.find_one({'Email':email})
    if user:
        flash("User already exits please login ","error")
        return redirect(url_for("auth.signup"))
    else:
        flash("Successfully register","success")
        collection.insert_one({"Name":name,"Email":email,'Password':generate_password_hash(password)})
        return redirect(url_for("auth.login"))


@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login",methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = collection.find_one({"Email":email})
    if user and check_password_hash(user["Password"],password):
        user_id = str(user['_id'])
        users = User(user_id)
        login_user(users)
        session['_id'] = user_id
        session['Name'] = user['Name']
        flash("Successfully login",'success')
        return redirect(url_for("main.profile"))
    else:
        flash("Not login",'error')
        return redirect(url_for("auth.login"))
    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('Name', None)
    session.pop('_id', None)
    flash("Successfully logout",'success')
    return redirect(url_for('auth.login'))
