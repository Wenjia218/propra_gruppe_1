#!/usr/bin/python3
import sys

import pymysql
import argparse as ap


def swissprot_in_db():
    # ___________Argument Parser:

    parser = ap.ArgumentParser()

    parser.add_argument('--input', type=ap.FileType("r"), default=sys.stdin)

    args = parser.parse_args()

    # _____________________________

    # connect to database
    db = pymysql.connect(host="mysql2-ext.bio.ifi.lmu.de", user="bioprakt01",
                         passwd="$1$io6mhFO5$MqQTA.eOzVMh2hDdllQij/",
                         database="bioprakt01")

    cursor = db.cursor()

    # ____________

    duplicate_id = []  # list of id's that are already in database and don't need to be added

    cursor.execute("SELECT ID FROM Sequences WHERE Source='Swissprot'")

    for row in cursor.fetchall():
        duplicate_id.append(row[-1])  # remove "," after ID and append to list  -> these need to be ignored


    duplicate_keywords = [] # list of keywords that are already in database and don't need to be added

    cursor.execute("SELECT * FROM Keywords")
    for row in cursor.fetchall():
        duplicate_keywords.append(row[-1])


    ac_value = ""  # strings to save the found lines in database
    kw_value = ""
    sq_value = ""
    os_value = ""
    source = "Swissprot"
    sq_start_val = False

    all_keywords = [] # list to save all keywords that were found in the process of saving the data from file

    for line in args.input:
        if line.startswith("AC"):
            line = line[2:]
            ac_values = line.split(";")
            ac_value = ac_values[0].strip()  # only take first AC number, because it is unambiguous identifier

        if line.startswith("KW"):
            line = line[2:]
            kw_value += line.replace("\n", "").replace(".", "")

        if line.startswith("OS"):
            line = line[2:]
            os_value += " " + line.replace("\n", "").replace(".", "").strip()

        if line.startswith("SQ"):
            sq_start_val = True  # indicates when to start reading sequence

        if sq_start_val == True and not line.startswith("SQ") and not line.startswith("//"):    # only read when not in first SQ line and at end
            sq_value += line.replace("\n", "").replace(" ", "")

        if line.startswith("//"):  # at the end of entry reset values in order to not have KW from previous

            sq_start_val=False # now stops reading sequence

            if ac_value != "" and ac_value not in duplicate_id: # deleting all entries without AC and when already saved in database

                # insert values into Sequences table in database:

                insert_query_sequences = """INSERT INTO Sequences VALUES(%s,%s,%s,%s)"""
                record1=(source,str(ac_value),sq_value,os_value)
                duplicate_id.append(ac_value)                       # add inserted ID into duplicate_Ids to guarantee unique ID insertion
                cursor.execute(insert_query_sequences,record1)



                # process kw_value in order to save it in a list for the Keywords and functions table

                keywords = kw_value.split(";")
                keyword_list = []  # in order to save keywords for this organism in functions table

                for keyword in keywords:
                    keyword_list.append(keyword.strip())
                all_keywords.extend(keyword_list)

                # loop for saving id with found keywords from keyword_list into functions table:

                insert_query_functions = """INSERT INTO functions VALUES(%s,%s,%s)"""

                for keyword in keyword_list:
                    record2 = (source,str(ac_value),str(keyword))
                    cursor.execute(insert_query_functions,record2)


            # reset values for next entry
            ac_value = ""
            kw_value = ""
            sq_value = ""
            os_value = ""


    # inserting all keywords that were found in Keywords table

    insert_query_keywords = """INSERT INTO Keywords VALUES(%s)"""

    # remove all duplicates from all_keywords:
    all_keywords = list(set(all_keywords))

    for keyword in all_keywords:
        if str(keyword) not in duplicate_keywords:

            record3 = (str(keyword))
            cursor.execute(insert_query_keywords,record3)


    cursor.close()


swissprot_in_db()
