from flask import Flask,redirect,url_for,request,render_template
from flask_sqlalchemy import SQLAlchemy
import os
project_dir=os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,"mydatabase.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file   #used to connect app with the database which we have created
db = SQLAlchemy(app)

#@app.route('/')
#def home():
#    return '<h1>This is HOme page</h1>'
class Book(db.Model):
    name = db.Column(db.String(100),unique=True,nullable=False,primary_key=True)
    author = db.Column(db.String(100),nullable=False)

@app.route('/profile/<uname>')
def profile(uname):
    #if 'isActive' is true it indicates that the user is successfully logged in
    return render_template('profile.html',uname=uname,isActive = False)

@app.route('/admin')
def welcome_admin():
    return 'Welcome Admin'

@app.route('/guest/<guest>')
def welcome_guest(guest):
    return 'Welcome Guest %s' %guest

@app.route('/user/<uname>')
def welcome_user(uname):
    if uname == 'admin':
        return redirect(url_for('welcome_admin'))
    else:
        return redirect(url_for('welcome_guest',guest=uname))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addbook')
def addbook():
    return render_template('addbook.html')

@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html',books = books)

@app.route('/submitbook', methods=['POST'])
def submitbook():
    name = request.form['name']
    author = request.form['author']
    book = Book(name=name,author=author)
    db.session.add(book)
    db.session.commit()
    return redirect('/books')

@app.route('/update',methods=['POST'])
def update():
    newname = request.form['newname']
    oldname = request.form['oldname']
    newauthor = request.form['newauthor']

    book = Book.query.filter_by(name=oldname).first()   #filer_by will retrieve all the records with the name equal to oldname
    book.name = newname
    book.author = newauthor
    db.session.commit()
    return redirect('/books')

@app.route('/delete',methods=['POST'])
def delete():
    name = request.form['name']
    book = Book.query.filter_by(name = name).first()
    db.session.delete(book)
    db.session.commit()

    return redirect('/books')

@app.route('/editbooks')
def editbook():
    books = Book.query.all()
    return render_template('editbooks.html', books=books)

if __name__ == "__main__":
 app.run(debug=True)     #debug=true --> helps us in making changes without restarting the server to see the changes

 SQLALCHEMY_TRACK_MODIFICATIONS = False