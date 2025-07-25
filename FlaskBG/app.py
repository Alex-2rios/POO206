from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Riosgamesas31@"
app.config['MYSQL_DB'] = "dbflask"
app.secret_key = "supersecretkey"

mysql = MySQL(app)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
