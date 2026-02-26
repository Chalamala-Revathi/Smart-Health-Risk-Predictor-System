from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",
    database="business_db"
)

cursor = db.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    values = (name, email, message)
    cursor.execute(sql, values)
    db.commit()

    return "Message stored successfully!"

if __name__ == "__main__":
    app.run(debug=True)
