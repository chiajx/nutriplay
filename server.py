## This code was written for Critical Making Provocation 2 by JXC, last updated April 2, 2018. This code runs on the server (aka my laptop, where the database is stored.) 

#!/usr/bin/env python

import socket
import csv


foodDict = {} #create empty dictionary

with open('database.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        print(row)
        row[0]
        foodDict[row[0]] = {'name':row[1], 'sugar': int(row[2])}

def scanUPC(barcode):
    print("received:")
    print(barcode)
    
    if barcode == "073310474106": #initialize with scanning the tissue box haha
        return 3

    if barcode not in foodDict:
        print("not recognized")
        return 4

    if foodDict[barcode]['sugar'] < 12:
        print("Good job" + foodDict[barcode]['name'] + "= healthy!")
        return 1

    elif foodDict[barcode]['sugar'] >= 12:
        print("Wah wah, this has lots of sugar... please try again!")
        return 2



TCP_IP = '192.168.1.101'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response (20 in example)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
 
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        barcode = conn.recv(BUFFER_SIZE)
        if not barcode: break
        print "received data:", barcode

        result = scanUPC(barcode)


        conn.send(str(result))  # echo
finally:
    s.close()
