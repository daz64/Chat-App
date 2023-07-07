from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.id

class Chat(db.Model):
    __bind_key__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    message =  db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, message):
        self.username = username
        self.message = message

    def __repr__(self):
        return '<Chat %r>' % self.id


@app.route("/")
def default():
    #db.drop_all()
    db.create_all()
    return redirect('/login//')

@app.route("/login/", methods = ['POST', 'GET'])
def login_controller():
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']
        try:
            user = User.query.filter_by(username=user_username).first_or_404() 
            if user.password == user_password:                                  
                return redirect('/profile/'+user.username)
            else:
                return redirect('/login/')
        except:                                                                 
            return redirect('/register')
    else:
        return render_template("loginPage.html")

@app.route("/register/", methods = ['POST', 'GET'])
def register_controller():
    if request.method == 'POST':
        user_username = request.form['username']
        user_email = request.form['email']
        user_password = request.form['password']
        user_repassword = request.form['repassword']
        if user_password == user_repassword: 
            try:
                user = User.query.filter_by(username=user_username).first_or_404()
                print("Username exists") #This occurs when the username already exists
                return redirect('/login/')
            except:
                new_user = User(username=user_username, email=user_email, password=user_password)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/profile/'+user_username)
                except:
                    return 'There was an issue adding your information'
        else:
            return redirect('/register/')
    else:
        return render_template("register.html")

@app.route("/logout/")
def unlogger():
    return redirect('/login/')

@app.route("/profile/<username>")
def profile(username=None):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("chat_page.html", user=user)

@app.route("/new_message/", methods = ['POST'])
def new_message():
    if request.method == 'POST':
        chat_username = request.form['username']
        new_message = request.form['message']
        new_chat = Chat(username=chat_username, message=new_message)
        try:
            db.session.add(new_chat)
            db.session.commit()
            return redirect('/messages/')
        except:
            return 'There was an issue adding your message'
    else:
        return request.method

@app.route("/messages/")
def messages():
    chat2 = []
    chat = Chat.query.order_by(Chat.date_created).all()
    for i in range(0, len(chat)):
        chat2.append({chat[i].username:chat[i].message})
    return json.dumps(chat2) 

if __name__ == "__main__":
    app.run(debug=True)


