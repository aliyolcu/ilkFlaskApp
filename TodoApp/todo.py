from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////./Users/ayolcu/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    kname = db.Column(db.String(80))
    sifre = db.Column(db.String(80))


@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)


@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    if ( todo.complete == False):
        todo.complete = True
    else:
        todo.complete = False

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()

    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add" , methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    content = request.form.get("content")

    newTodo = Todo(title = title , content = content , complete = False)

    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/kullaniciKayit")
def kKayitG():

    return render_template("kKayit.html")

@app.route("/kayit", methods = ["POST"])
def kKayit():

    kname = request.form.get("kname")
    sifre = request.form.get("sifre")

    newKullanici = User(kname = kname , sifre = sifre)

    db.session.add(newKullanici)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/kullanici")
def kGiris():

    todos = User.query.all()
    return render_template("KGiris.html", todos = todos)

@app.route("/deneme" ,methods=["GET","POST"])
def deneme():
   
    if request.method == "POST":
        todos = Todo.query.all()
        kname = request.form.get("kname")
        sifre = request.form.get("sifre")

        VeriAd = User.query.filter_by(kname=kname).first()
        VeriSifre = User.query.filter_by(sifre=sifre).first()
        db.session.commit()

        if VeriAd.kname == kname and VeriSifre.sifre == sifre:
            return render_template("index.html" , kname = kname , sifre = sifre , todos = todos)
        else: 
             return render_template("index.html")
    else:
         return render_template("index.html")




if __name__ == "__main__":
    app.run(debug = True)