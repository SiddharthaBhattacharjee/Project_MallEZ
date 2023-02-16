import mysql.connector as sql

def create_database(password):

   pw = password
   try:
       conn=sql.connect(host='localhost',user='root',password=pw,charset='utf8')
       mycursor=conn.cursor()
   except:
      print("Password Incorrect!")
   conn.autocommit = True
   mycursor.execute("create database mallDatabase")
   mycursor.execute("use mallDatabase")
   mycursor.execute("create table data(user_id varchar(20) primary key ,time varchar(40))")
