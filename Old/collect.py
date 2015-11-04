### First block to replace

import glob
import os
import mysql.connector

def UpdateDatabase(nowdir,DataDir):

    # Get time sorted list of available files in current day
    DirToSearch = DataDir + nowdir + '/data*'
    files = glob.glob(DirToSearch)   
    files.sort(key=os.path.getmtime)
    if os.path.getsize(files[len(files)-1])>0: # Test if there was something in the last recorded data file  
        try:
	    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cnx = mysql.connector.connect(host="panyagua.nl", # your host, usually localhost
	        port=3306, # port name
	        user="seti", # your username
	        passwd="seti1", # your password
	        database="seti") # name of the data base
	    cursor = cnx.cursor()
	    cursor.execute("INSERT INTO candidates (DateTimeInsert, DishLocation, DataFileName) " +
		                  "VALUES ('" + now + "','" + 'Ijsselstein' + "','" + os.path.abspath(files[len(files)-1]) + "')")
	    cnx.commit()
	    cursor.close()
	    cnx.close()
	    print('Data uploaded to database [OK]')
	except mysql.connector.Error as err:
	    print("Could not connect to database [NOK]")
    return

#### Second block to replace
    
    UpdateRate = 5*60 # In seconds
    DataDir = '/media/michel/SETI/'
    # Repeat forever
    while True:

        # start and wait untill next period
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nowdir = datetime.now().strftime("%Y/%Y%m%d")
        print(now + ' Started new file')
        tb.start()
        while True:
            NumSeconds = int(time.strftime("%M"))*60+int(time.strftime("%S"))
            if NumSeconds % UpdateRate ==0:
                UpdateDatabase(nowdir, DataDir)
                tb.set_prefix(DataDir + datetime.now().strftime("%Y/%Y%m%d"))
                time.sleep(1)
                break
            time.sleep(1)
        tb.stop()
        tb.wait()
