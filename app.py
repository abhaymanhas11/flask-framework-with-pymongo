from flask import Flask,render_template,request,redirect
import pymongo
app=Flask(__name__)

try:
    client=pymongo.MongoClient("mongodb://localhost:27017")
    db=client["test"]
    collection = db['abhay']
except:
    print("not conected")

@app.route('/',methods=['POST','GET'])
def add():
    if request.method=="POST":
        nam=request.form["name"]
        cla=request.form["class"]
        ph=request.form["phone"]
        dict={"name":nam,"class":cla,"phone":ph}
        collection.insert_one(dict)
        return redirect('/')
    else:
        x = collection.find()

        return render_template('adduser.html',alluser=x)

@app.route('/delete/<name>',methods=['GET'])
def delete(name):
    collection.delete_one({"name":name})
    return redirect('/')

@app.route('/update/<phone>',methods=['POST','GET'])
def update(phone):
    if request.method=="POST":
        dict = collection.find_one({"phone": phone})
        nam = request.form["name"]
        cla = request.form["class"]
        ph = request.form["phone"]
        newdict = {"$set":{"name": nam, "class": cla, "phone": ph}}
        collection.update_one(dict,newdict)
        return redirect('/')
    else:
        x = collection.find_one({"phone": phone})
        return render_template('update.html', alluser=x)

@app.route('/search',methods=['POST','GET'])
def search():
    if request.method =='POST':
        n=request.form["sname"]
        x=collection.find({"name": n})
        return render_template('search.html',searchuser=x)

    return render_template('search.html')


if __name__=="__main__":
     app.run(debug=True)