"""
  * Author :Ravindra
  * Date   :23-11-2020
  * Time   :19:58
  * Package:curdoperation
  * Statement:Curd Operation Using Flask
"""
from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import os

from jinja2 import UndefinedError

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ['user']
app.config['MYSQL_PASSWORD'] = os.environ['password']
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def home():
    """Method Definition
       Home page
       return Template
    """
    if request.form:
        print(request.form)
    return render_template("home.html")

@app.route('/createTable', methods=['GET', 'POST'])
def createTable():
    """Method Definition
         create Table In Database
         :return template
      """
    try:
        if request.method == "POST":
            cursor = mysql.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS students1 (name VARCHAR(25), address VARCHAR(25))")
            cursor.close()
            return "Table created successfully"
        return render_template("create.html")
    except request.exceptions.RequestException as e:
        mysql.connection.rollback()
        return e
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    """Method Definition
       Insert records into Table In Database
       :return template
    """
    try:
        if request.method == "POST":
            name = request.form['name']
            address = request.form['address']

            cursor = mysql.connection.cursor()
            sql = "INSERT INTO students (name, address) VALUES (%s, %s)"
            val = (name, address)
            cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()
            return "Data Inserted successfully"
        return render_template("insert.html")
    except request.exceptions.RequestException as e:
        mysql.connection.rollback()
        return e
@app.route('/showdata')
def getRecords():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()
        cursor.close()
        return render_template("show.html", data=data)
    except request.exceptions.RequestException as e:
        mysql.connection.rollback()
        return e

@app.route('/update', methods=['GET', 'POST'])
def update():
    """Method Definition
       Update Records into Table In Database
       :return template
    """
    try:
        if request.method == "POST":
            if request.form['update']:
                name = request.form['name']
                address = request.form['address']
                id=request.form['id']
                cursor = mysql.connection.cursor()
                sql = "UPDATE students SET name  = %s, address= %s WHERE id = %s"
                val = (name,address,id )
                a = cursor.execute(sql, val)
                mysql.connection.commit()
                cursor.close()
                if a == 1:
                    return "Student data Updated Successfully"
                else:
                    return "Student data Not Updated"
        return render_template("update.html")
    except request.exceptions.RequestException as e:
        mysql.connection.rollback()
        return e

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """Method Definition
       Delete Records from Table In Database
       :return Template
    """
    try:
        if request.method == "POST":
            id = int(request.form['id'])
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM students WHERE id = %s"
            val = (id,)
            a=cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()
            if a == 1:
                return "Student data Deleted Successfully"
            else:
                return "Student data Not Deleted"
        return render_template("delete.html")
    except request.exceptions.RequestException as e:
        mysql.connection.rollback()
        return ""

if __name__ == "__main__":
    """Main Method"""
    app.run(debug=True)