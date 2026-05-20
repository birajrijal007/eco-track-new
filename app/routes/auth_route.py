from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql, bcrypt

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                      (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and bcrypt.check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["role"] = user[4]
            flash("Login successful!", "success")
            return redirect(url_for("home.dashboard"))
        else:
            flash("Wrong email or password!", "danger")
    
    return render_template("auth/login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))