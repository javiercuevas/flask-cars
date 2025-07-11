#import pyodbc
#import pandas as pd
from flask import (Flask, render_template, request, url_for, flash, redirect)
from werkzeug.exceptions import abort
from models.car import Car


#https://absolutecodeworks.com/python-flask-crud-sample-with-sql-server
#https://chuckpr.github.io/posts/fivethirtyeight-tables/


app = Flask(__name__)
app.config['SECRET_KEY'] = 'rhs83kjsoih!'


#######################################################
# routes
#######################################################
@app.route('/')
def index():
    #sql = "select * from dbo.Cars"
    car = Car()
    cars = car.get_cars()
    return render_template("carlist.html", cars = cars)



@app.route("/addcar", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html", car = {})
    if request.method == 'POST':
        #form
        id = int(request.form["id"])
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])

        #conn = connection()
        #cursor = conn.cursor()
        #cursor.execute("INSERT INTO dbo.TblCars (id, name, year, price) VALUES (?, ?, ?, ?)", id, name, year, price)
        #conn.commit()
        #conn.close()

        #sql = f"insert into dbo.Cars (id, name, year, price) values ({id}, '{name}', {year}, {price})"
        #query_execute_nonquery(sql)

        car = Car()
        car.add_car(id=id, name=name, year=year, price=price)
        return redirect('/')


@app.route('/updatecar/<int:id>',methods = ['GET','POST'])
def updatecar(id):
    car = Car()
    if request.method == 'GET':
        #sql = f"SELECT * FROM dbo.Cars WHERE id = {id}"
        #car = query_execute(sql)
        car = car.get_car(id=id)
        if len(car) == 0:
            flash('No record found', 'danger')
        return render_template("addcar.html", car = car)

    if request.method == 'POST':
        name = str(request.form["name"])
        year = int(request.form["year"])
        price = float(request.form["price"])
        #sql = f"UPDATE dbo.Cars SET name = '{name}', year = {year}, price = {price} WHERE id = {id}"
        #query_execute_nonquery(sql)
        car.update_car(id=id, name=name, year=year, price=price)
        flash(f'Record updated: {name}')
        return redirect('/')
    

@app.route('/deletecar/<int:id>')
def deletecar(id):
    #sql = f"DELETE FROM dbo.Cars WHERE id = {id}"
    #query_execute_nonquery(sql)
    car = Car()
    car.delete_car(id=id)
    return redirect('/')


#######################################################
# error handlers
#######################################################
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


#######################################################
# run app
#######################################################
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)