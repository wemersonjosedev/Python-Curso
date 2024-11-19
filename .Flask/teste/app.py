from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/carreira_python"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM vagas"))
        results = result.fetchall()
        column_names = result.keys()
        results_dict = [dict(zip(column_names, row)) for row in results]
    return jsonify(results_dict)

if __name__ == '__main__':
    app.run(debug=True)
