import mysql.connector as sql

def create_database(password):

   pw = password
   try:
       conn=sql.connect(host='localhost',user='root',password=pw,charset='utf8')
       mycursor=conn.cursor()
   except:
      print("Password Incorrect!")
   conn.autocommit = True
   mycursor.execute("create database MallEZ_Admin_Database")
   mycursor.execute("use MallEZ_Admin_Database")
   mycursor.execute("create table data(business_ID varchar(40) primary key ,business_Name varchar(40))")
