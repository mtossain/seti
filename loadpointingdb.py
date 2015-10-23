from xml.dom.minidom import parse
import mysql.connector
import xml.dom.minidom

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("/media/michel/SETI/script.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("Script"):
   print ("Root element : %s" % collection.getAttribute("Script"))

# Get all the movies in the collection
Passes = collection.getElementsByTagName("Pass")
cnt=1
for Pass in Passes:
   cnt=cnt+1
   print(str(cnt))
   StartPass = Pass.getElementsByTagName('StartPass')[0]
   StartPassStr=str(StartPass.childNodes[0].data)
   StopPass = Pass.getElementsByTagName('StopPass')[0]
   StopPassStr=str(StopPass.childNodes[0].data)
   RightAscension = Pass.getElementsByTagName('RightAscension')[0]
   RightAscensionStr=str(RightAscension.childNodes[0].data)
   Declination = Pass.getElementsByTagName('Declination')[0]
   DeclinationStr= str(Declination.childNodes[0].data)
   Duration = Pass.getElementsByTagName('Duration')[0]
   DurationStr=str(Duration.childNodes[0].data)
   NameTarget = Pass.getElementsByTagName('NameTarget')[0]
   NameTargetStr=str(NameTarget.childNodes[0].data)

   try:
        cnx = mysql.connector.connect(
		         host="panyagua.nl", # your host, usually localhost
		         port=3306, # port name
		         user="seti", # your username
		         passwd="seti1", # your password
		         database="seti") # name of the data base
        cursor = cnx.cursor()
        sql = "INSERT INTO pointing (StartPass, StopPass, RightAscension, Declination, Duration, NameTarget) "
        sql = sql + "VALUES ('" + StartPassStr + "','" +StopPassStr+ "','" + RightAscensionStr + "','"
        sql = sql + DeclinationStr+ "','"+ DurationStr+         "','"+NameTargetStr+ "')"
        #print(sql)
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close()
        print('Data uploaded to database [OK]')
   except mysql.connector.Error as err:
        print("Could not connect to database [NOK]")
