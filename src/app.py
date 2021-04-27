import os
import socket
import loginQueries as lq
import requestQueries as rq
import initializedatabase as init
from flask import Flask, render_template, redirect, request, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "135789023949273alsdkjalskdfj")
chat_messages = [] # Message yang diperlihatkan List of dictionary: {name, message, time}
timeformat = "%H:%M:%S" # Format waktu
dateformat = "%Y-%m-%d" # Format tanggal

# Menambahkan message pada list chat_messages
def add_chat(name, message):
    chat_messages.append({"name": name, "message": message, "time": datetime.now().strftime(timeformat)})
    return

# Login Page
@app.route('/', methods = ["GET", "POST"])
def home():
    error = ""
    if "email" in session:
        return redirect(url_for('about')) # Ganti
    if request.method == "POST":
        if not request.form["email"] or not request.form["password"]:
            error = "Please enter email and password"
        elif not lq.isEmailExist(request.form["email"]):
            error = "Email not registered, please register first"
        elif lq.getLoginInfo(request.form["email"]) != request.form["password"]:
            error = "Incorrect password"
        elif lq.getLoginInfo(request.form["email"]) == request.form["password"]:
            session["email"] = request.form["email"]
            return redirect(url_for('about')) # Placeholder

    return render_template('login.html', error = error)

# Register page
@app.route('/register', methods = ["GET", "POST"])
def register():
    error = ""
    if "email" in session: # not working
        return redirect(url_for('about')) # Ganti
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
            return redirect(url_for('home'))
    return render_template('register.html', error = error)

# Chat Page
@app.route('/chat/<user_id>', methods = ["GET", "POST"])
def chat(user_id):
    return render_template('homepage.html') # Placeholder

# About Page (static)
@app.route('/about')
def about():
    return render_template('homepage.html') # Placeholder

# Instructions Page (static) # Mungkin ga dipake
@app.route('/instructions')
def instructions():
    return render_template('homepage.html') # Placeholder

if __name__ == "__main__":
    # app.run(host = '192.168.100.2', port = 5000, debug = False)
    app.run(debug = True)