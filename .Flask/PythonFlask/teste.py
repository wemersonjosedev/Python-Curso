from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)
app.secret_key = 'fd7f67f7edae58cd2ec220a1de9d03fc'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/cursos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

with db.engine.connect() as conn:
    result = conn.execute("SELECT * FROM user")
    for row in result:
        print(row)
