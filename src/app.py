from flask import Flask, render_template
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

if __name__ == "__main__":
    # app.run(host = '192.168.100.2', port = 5000, debug = False)
    app.run()