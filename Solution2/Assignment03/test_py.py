#!/usr/bin/python3
import pymysql

db=pymysql.connect(host="localhost",port=3307, user="bioprakt01",
passwd='$1$io6mhFO5$MqQTA.eOzVMh2hDdllQij/',database="bioprakt01")

cursor=db.cursor()

cursor.execute("select * from Sequences")
for row in cursor.fetchall():
   print(row)
db.close()