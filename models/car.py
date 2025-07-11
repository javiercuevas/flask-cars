from dataclasses import dataclass
import pyodbc
import pandas as pd


def cstr():
    s = 'localhost\sql2019'
    d = 'CarSales' 
    u = 'sa'
    p = 'javi01'
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    return cstr


def query_execute(sql: str, cstr: str = cstr()):
    sql = sql.strip()
    with pyodbc.connect(cstr) as conn:
        df = pd.read_sql_query(sql, conn)
    res = df.to_dict(orient='records')
    return res


def query_execute_nonquery(sql: str, cstr: str = cstr()):
    import pyodbc
    #execute sql statement
    conn = pyodbc.connect(cstr)
    #execute sql
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute(sql)
    #conn.commit()
    #close conn
    conn.close()


@dataclass
class Car():

    def get_cars(self):
        #sql = "select * from dbo.Cars"
        sql = "exec usp_CarsGet"
        cars = query_execute(sql)
        return cars


    def get_car(self, id: int):
        sql = f"select * from dbo.Cars where id = {id}"
        car = query_execute(sql)
        if len(car) > 0:
            return car[0]
        else:
            return {}


    def add_car(self, id: int, name: str, year: int, price: int):
        sql = f"insert into dbo.Cars (id, name, year, price) values ({id}, '{name}', {year}, {price})"
        query_execute_nonquery(sql)
        return


    def update_car(self, id: int, name: str, year: int, price: int):
        sql = f"update dbo.Cars set name = '{name}', year = {year}, price = {price} where id = {id}"
        query_execute_nonquery(sql)
        return


    def delete_car(self, id: int):
        sql = f"delete from dbo.Cars where id = {id}"
        query_execute_nonquery(sql)
        return