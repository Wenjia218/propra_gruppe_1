#!/usr/bin/python3
import sys

import pymysql
import argparse as ap


def swissprot_in_db():
    # connect to database
    db = pymysql.connect(host="127.0.0.1", user="bioprakt01", passwd="$1$io6mhFO5$MqQTA.eOzVMh2hDdllQij/",
                         database="bioprakt01", port=3308)

    cursor = db.cursor()


    duplicate_keywords = [] # list of keywords that are already in database and don't need to be added

    cursor.execute("SELECT * FROM Keywords")
    for row in cursor.fetchall():
        duplicate_keywords.append(row[-1])

    cursor.close()

    print(duplicate_keywords)

swissprot_in_db()