from flask import Flask, render_template, request, redirect
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mysql_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():

    connection = pymysql.connect(**mysql_config)
    connection.close()

    return render_template('login.html')

@app.route('/')
def home():
    connection = pymysql.connect(**mysql_config)
    connection.close()
    return render_template('home.html')

if __name__ == '__main__':
    app.run()