from flask import Flask, render_template, redirect, request, flash
import re
from mysqlconnection import MySQLConnector  
app = Flask(__name__)
app.secret_key = "benjiChippers"
mysql = MySQLConnector(app, "validator")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
	EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
	
	if EMAIL_REGEX.match(request.form['email']):
		query = "INSERT INTO users (email_address, created_at, updated_at) VALUES (:email_address, NOW(), NOW())"
		
		
		data = {"email_address": request.form['email']}
		
		newuserid = mysql.query_db(query, data)
		flash("The Email Entered ({}), is a Valid Email Address".format(request.form["email"]))
		print "We have a vaild email", newuserid
		return redirect("/success")
	else:
		print "Not a vaild email"
		flash("Not a valid email")
	
	return redirect("/")

@app.route("/success")
def success():
	allemails = mysql.query_db("SELECT * FROM users")
	print "all the emails", allemails
	return render_template("success.html", users = allemails)

app.run(debug=True)