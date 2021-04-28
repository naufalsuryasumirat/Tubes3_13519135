import os
import socket
import loginQueries as lq
import requestQueries as rq
import initializedatabase as init
import backend as bd
from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "135789023949273alsdkjalskdfj")
chat_messages = [[] for i in range(lq.userCount())] # Message yang diperlihatkan List of dictionary: {name, message, time}
timeformat = "%H:%M:%S" # Format waktu
dateformat = "%Y-%m-%d" # Format tanggal

# Menambahkan message pada list chat_messages
def add_chat(name, message, user_id):
    chat_messages[user_id].append({"name": name, "msg": message, "time": datetime.now().strftime(timeformat)})
    return

# Mengubah string untuk ditampilkan pada website
def convertmessage(input):
    return input.replace("\n", "<br/>")

# Login Page
@app.route('/', methods = ["GET", "POST"])
def home():
    error = ""
    if "email" in session:
        return redirect(url_for('chat', user_id = lq.getUserID(session["email"]))) # Ganti
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if not email or not password:
            error = "Please enter email and password"
        elif not lq.isEmailExist(email):
            error = "Email not registered, please register first"
        elif lq.getLoginInfo(email) != password:
            error = "Incorrect password"
        elif lq.getLoginInfo(email) == password:
            session["email"] = email
            return redirect(url_for('chat', user_id = lq.getUserID(email))) # Placeholder

    return render_template('login.html', error = error)

# Register page
@app.route('/register', methods = ["GET", "POST"])
def register():
    global chat_messages
    error = ""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        if not name or not email or not password:
            error = "Please input all valid credentials"
        elif lq.isEmailExist(request.form["email"]):
            error = "Email already registered, please login"
        else:
            lq.addUserEntry(name, email, password)
            chat_messages2 = [[] for i in range(lq.userCount())]
            for i in range(len(chat_messages)):
                chat_messages2[i] = chat_messages[i]
            chat_messages = chat_messages2
            return redirect(url_for('home'))
    return render_template('register.html', error = error)

# Chat Page
@app.route('/chat/<user_id>', methods = ["GET", "POST"])
def chat(user_id):
    name = lq.getNameID(user_id)
    if request.method == "POST":
        message = request.form["message"]
        name = lq.getNameID(user_id)
        add_chat(name, message, (int(user_id) - 1))
        add_chat('bot', bd.get_bot_message(message, int(user_id)).replace("\n", "<br>"), (int(user_id) - 1))
        
    return render_template('chat.html', name = name, messages = chat_messages[int(user_id) - 1]) # Placeholder

# About Page (static)
@app.route('/about')
def about():
    return render_template('homepage.html') # Placeholder

if __name__ == "__main__":
    app.run(host = '192.168.100.2', port = 80, debug = True, threaded = True)
    # app.run(debug = True)