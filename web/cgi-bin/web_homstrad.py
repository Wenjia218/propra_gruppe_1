#!/usr/bin/python3
import argparse
import os
import pymysql

parser = argparse.ArgumentParser()
parser.add_argument('--id')
args = parser.parse_args()
ID = args.id

db = pymysql.connect(host="mysql2-ext.bio.ifi.lmu.de", database="bioprakt01", user="bioprakt01", password="$1$io6mhFO5$MqQTA.eOzVMh2hDdllQij/")
cursor = db.cursor()
sql = """SELECT Sequence FROM Alignments WHERE Term="secondary structure and phi angle" AND ProteinID = (%s);"""

if "," not in ID:
    # write into mysql
    cursor.execute(sql, ID)
    print(ID)
    print(cursor.fetchall())
else:
    has_family = False
    ID1 = ID.split(",")[0].strip()
    ID2 = ID.split(",")[1].strip()
    sqlf = """SELECT Family FROM Alignments WHERE Term="secondary structure and phi angle" AND ProteinID = (%s);"""
    cursor.execute(sqlf, ID1)
    families1 = cursor.fetchall()
    cursor.execute(sqlf, ID2)
    families2 = cursor.fetchall()
    for family in families1:
        for f in families2:
            if family == f:
                has_family = True
                sql12 = """SELECT Sequence FROM Alignments WHERE Term = "secondary structure and phi angle" AND ProteinID = (%s) AND Family = (%s)"""
                line1 = (ID1, family)
                cursor.execute(sql12, line1)
                print(family)
                print(ID1 + ": ")
                print(cursor.fetchall())
                line2 = (ID2, family)
                cursor.execute(sql12, line2)
                print(ID2 + ": ")
                print(cursor.fetchall())
    if not has_family:
        print("Keine gemeinsame Family")
        cursor.execute(sql, ID1)
        print(ID1)
        print(cursor.fetchall())
        cursor.execute(sql, ID2)
        print(ID2)
        print(cursor.fetchall())












