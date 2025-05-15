#!/usr/bin/python3
import os
import pymysql

def read_ali(file):
    lines = []
    for line in file:
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    return lines

def read_tem(file):
    alignment = {}
    start = False
    for line in file:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            start = True
            ID = line[1:]
            continue
        elif start == True:
            start = False
            tem = line
            key = ID + "-" + tem
            if key not in alignment:
                alignment[key] = ""
                continue
        sequence = line
        alignment[key] = alignment[key] + sequence
    return alignment



# get all Alignments from HOMSTRAD
path = "/mnt/biocluster/praktikum/bioprakt/Data/HOMSTRAD"
dir_list = os.listdir(path)

# write into mysql
db = pymysql.connect(host="127.0.0.1", port=3307, database="bioprakt01", user="bioprakt01", password="$1$io6mhFO5$MqQTA.eOzVMh2hDdllQij/")
cursor = db.cursor()
sql = """INSERT INTO Alignments VALUES (%s, %s, %s, %s);"""

for file_name in dir_list:
    if file_name != "d" and file_name != "du" and file_name != "x" and file_name != "y" and file_name != "z":
        path2 = path + '/' + file_name
        dir_list2 = os.listdir(path2)
        family = ""
        for file in dir_list2:
            alignment = {} # key: proteinID+term, value : seq
            if file.endswith(".ali"):
                ali = path2 + "/" + file
                with open(ali, "r") as f:
                    alignment = read_ali(f)
                    for line in alignment:
                        if "family" in line:
                            family = line.split(":")[1].strip()
                            break
            if file.endswith(".tem"):
                tem = path2 + "/" + file
                with open(tem, "r") as f:
                    alignment = read_tem(f)
                for key in alignment:
                    term = key.split("-")[1]
                    if term == "sequence" or term == "secondary structure and phi angle":
                        ID = key.split("-")[0]
                        seq = alignment[key]
                        if not family == "":
                            record = (family, ID, term, seq)
                        else:
                            record = ("igcon", ID, term, seq)
                        cursor.execute(sql, record)










