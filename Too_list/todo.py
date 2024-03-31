from flask import Flask, flash, redirect,request, render_template, url_for,Blueprint,session
from datetime import datetime
from flask_login import login_required
from Mongodb import * 
from bson import ObjectId
todo = Blueprint("user_todo",__name__)


@todo.route("/delete/<userid>")
@login_required
def delete(userid):
    if "Name" in session and "_id" in  session:
        user_todo.delete_one({"_id":ObjectId(userid)})
    return redirect(url_for("main.profile"))

@todo.route("/update/<userid>",methods=['POST','GET'])
@login_required
def update(userid):
    if request.method == "POST":
        title = request.form.get("title")
        todo = request.form.get("todo")
        current_date = datetime.now().strftime('%d/%m/%Y,%I:%M %p')
        if user_todo.find_one({"_id":ObjectId(userid)}):
            user_todo.update_many({"_id":ObjectId(userid)},{"$set":{"Title":title,"Todo":todo,"Time":current_date,"Edit":"(edit)"}})
            return redirect(url_for('main.profile'))
        else:
            return "some thing error"
    user = user_todo.find_one({"_id":ObjectId(userid)})
    return render_template ("todo_update.html",user=user)
        