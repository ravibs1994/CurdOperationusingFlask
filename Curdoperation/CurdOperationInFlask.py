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

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Method Definition
         create Table In Database
         :return template
      """
    if request.method == "POST":
      cursor = mysql.connection.cursor()
      cursor.execute("CREATE TABLE IF NOT EXISTS students1 (name VARCHAR(25), address VARCHAR(25))")
      cursor.close()
      return "Table created successfully"
    return render_template("create.html")

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    """Method Definition
       Insert records into Table In Database
       :return template
    """
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

@app.route('/get')
def getRecords():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cursor.close()
    return render_template("show.html", data=data)

@app.route('/update', methods=['GET', 'POST'])
def update():
    """Method Definition
       Update Records into Table In Database
       :return template
    """
    if request.method == "POST":
        if request.form['update']:
            name = request.form['name']
            address = request.form['address']
            id=request.form['id']
            cursor = mysql.connection.cursor()
            sql = "UPDATE students SET name  = %s, address= %s WHERE id = %s"
            val = (name,address,id )
            cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()
        return "updated successfully"
    return render_template("update.html")

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """Method Definition
       Delete Records from Table In Database
       :return Template
    """
    if request.method == "POST":
        id = request.form['id']
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM students WHERE id = %s"
        val = (id,)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return "delete successfully"
    return render_template("delete.html")

if __name__ == "__main__":
    """Main Method"""
    app.run(debug=True)