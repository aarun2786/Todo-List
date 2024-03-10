from flask import Flask,redirect,request,render_template,url_for
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client['USERBASE']
collection = db['user_data']

@app.route("/",methods=['POST','GET'])
def get_data():
    if request.method == 'POST':
        Title = request.form['Title'].title()
        Todo = request.form['Todo']
        current_date = datetime.now().strftime('%d/%m/%Y,%I:%M %p')
        collection.insert_one({"Title":Title,"Todo":Todo,"Time":current_date})
        
    data = collection.find()
    return render_template("home.html",datas =data)


@app.route("/delete/<id>")
def delete_data(id):
    collection.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('get_data'))

@app.route("/edit/<id>",methods=['GET','POST'])
def edit_data(id):
    if request.method=='POST':
        #ids = request.form['user_id']
        Title = request.form['Title'].title()
        Todo = request.form['Todo']
        current_date = datetime.now().strftime('%d/%m/%Y,%I:%M %p') 
        if collection.find_one({"_id":ObjectId(id)}):
            collection.update_many({"_id":ObjectId(id)},{"$set":{"Title":Title,"Todo":Todo,"Time":current_date,"Edit":"(edit)"}})
            return redirect("/")
        else:
            return "Not find"
    update_data = collection.find_one({"_id":ObjectId(id)})
    return render_template("update.html",update_data=update_data)

if __name__=='__main__':
    app.run(debug=True)
    