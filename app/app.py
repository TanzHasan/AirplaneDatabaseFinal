from flask import Flask
import pymysql
import os
from dotenv import load_dotenv

app = Flask(__name__)
@app.route('/')
def home():
    return

if __name__ == '__main__':
    app.run()