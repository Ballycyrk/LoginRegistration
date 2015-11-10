from flask import Flask, flash, session, request, render_template, redirect
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re
NAME_REGEX = pass
EMAIL_REGEX = pass
PW_REGEX = pass
app = Flask(__name__)
app.secret_key = 'InvestED'

@app.route('/')
def index():
  return render_template('index_html')

app.run(debug=True)

