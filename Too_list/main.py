from flask import Blueprint,render_template,url_for,session,request,redirect
import datetime
from flask_login import current_user,login_required,logout_user
main = Blueprint('main',__name__)
from Mongodb import *
from bson import ObjectId
@main.route('/')
def home():
    logout_user()
    return render_template("home.html")

@main.route('/profile')
@login_required
def profile():
    if "Name" in session:
        user = session.get("Name")
        todo = user_todo.find({"Name": user})
        return render_template("profile.html", todos=todo,name=user)

@main.route("/todos",methods=['POST'])
@login_required
def todo():
    try:
        if "Name" and "_id" in session:
            user = session['Name']
            user_id = session['_id']
            title = request.form.get("title")
            todo = request.form.get("todo")
            time = datetime.datetime.now()
            dt = time.strftime('%d/%m/%Y,%I:%M:%p')
            user_todo.insert_one({"Name":user,"Title":title,"Todo":todo,"Time":dt})
            return redirect(url_for("main.profile"))
    except:
        return redirect(url_for("auth.login"))
@main.route("/profileview")
@login_required
def profile_view():
    try:
        if "Name" and '_id' in session:
            user = session.get('Name')
            users = collection.find({"Name":user})
            return render_template("viewprofile.html",users=users)
    except Exception as e :
        return redirect(url_for("auth.login"))