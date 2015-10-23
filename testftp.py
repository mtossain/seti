import glob
import os
import mysql.connector
import datetime
import time
from datetime import datetime

def UpdateDatabase(now,DataDir):

    # Get time sorted list of available files in current day
    DirToSearch = DataDir + time.strftime("%Y/%Y%m%d") + '/data*'
    files = glob.glob(DirToSearch)   
    files.sort(key=os.path.getmtime)

    if os.path.getsize(files[len(files)-1])==0: # Test if there was something in the last recorded data file  
        try:
            cnx = mysql.connector.connect(
		         host="panyagua.nl", # your host, usually localhost
		         port=3306, # port name
		         user="seti", # your username
		         passwd="seti1", # your password
		         database="seti") # name of the data base
            cursor = cnx.cursor()
            cursor.execute("INSERT INTO seti (DateTimeInsert, DishLocation, DataFileName) " +
		                  "VALUES ('" + now + "','" + 'Ijsselstein' + "','" + os.path.abspath(files[len(files)-1]) + "')")
            cnx.commit()
            cursor.close()
            cnx.close()
            print('Data uploaded to database [OK]')
        except mysql.connector.Error as err:
            print("Could not connect to database [NOK]")
    return

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
DataDir = '/media/michel/SETI/'
UpdateDatabase(now,DataDir)
