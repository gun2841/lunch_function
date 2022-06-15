import cx_Oracle
import csv
import os
import time
def insertLunch(dfs):
    location = r"C:\oracle\instantclient_11_2"
    os.environ["PATH"] = location + ";" + os.environ["PATH"]
    dsn = cx_Oracle.makedsn("192.168.0.205", 1521, service_name="NEMI")  # 오라클 주소
    connection = cx_Oracle.connect(user="SCOTT", password="1", dsn=dsn, encoding="UTF-8")  # 오라클 접속
    columns = ['', 'stores', 'X', 'Y', 'category', 'road_address', 'place_url']
    cur = connection.cursor()
    for i in range(len(dfs)):
        sql = f"INSERT INTO SCOTT.LUNCHMENU (RSTRTIDX, NAME, RATING, CLASSIFICATION, ADDRESS)" \
              f"values ( {dfs['ID'][i]}, '{dfs['stores'][i]}','{dfs['rating'][i]}','{dfs['category'][i]}'" \
              f",'{dfs['road_address'][i]}' )"
        print(sql)
        cur.execute(sql)
        connection.commit()
        time.sleep(0.01)
def insertFood(dfs):
    location = r"C:\oracle\instantclient_11_2"
    os.environ["PATH"] = location + ";" + os.environ["PATH"]
    dsn = cx_Oracle.makedsn("192.168.0.205", 1521, service_name="NEMI")  # 오라클 주소
    connection = cx_Oracle.connect(user="SCOTT", password="1", dsn=dsn, encoding="UTF-8")  # 오라클 접속
    columns = ['', 'stores', 'X', 'Y', 'category', 'road_address', 'place_url']
    cur = connection.cursor()
    for i in range(len(dfs)):
        if len(dfs['menu'][i]) == 0: continue

        for li in dfs['menu'][i]:
            sql = f"INSERT INTO SCOTT.FOODPRICE  " \
                  f"  (MENUIDX, RSTRTIDX, MENUNAME, PRICE)" \
                  f"        VALUES({i}, {dfs['ID'][i]}, '{li[0]}', '{li[1]}')"
            cur.execute(sql)
            connection.commit()
            time.sleep(0.01)