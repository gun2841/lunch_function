import cx_Oracle
import csv
import os
import time
location =r"C:\oracle\instantclient_11_2"
os.environ["PATH"]=location+";"+os.environ["PATH"]
dsn = cx_Oracle.makedsn("192.168.0.205", 1521, service_name = "NEMI") # 오라클 주소
connection = cx_Oracle.connect(user="SCOTT", password="1", dsn=dsn, encoding="UTF-8") # 오라클 접속

cur = connection.cursor()

f = open('test.csv','r',encoding="utf-8")
rdr =csv.reader(f)
for id,line in enumerate(rdr):
    if id ==0: continue
    addr = str(line[4]).split('\n')[1]
    sql = f"INSERT INTO SCOTT.LUNCHMENU (RSTRTIDX, NAME, RATING, CLASSIFICATION, ADDRESS)" \
          f"values ( {id+4}, '{line[0]}' ,'{line[1]}' ,'{line[5]}' ,'{addr}' )"
    print(sql)
    cur.execute(sql)
    connection.commit()
    time.sleep(0.01)