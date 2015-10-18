import os
import time

# At start do until next hour
mintogo = 60-int(time.strftime("%M"))-3
now = time.strftime("_%Y%m%d_%H")
command = "rtl_power -f 1415M:1425M:5k -i 10 -g 50 -c 0.40 -e "+str(mintogo)+"m data"+now+".csv"
print (time.strftime("%Y-%m-%d %H:%M:%S ") + command)
os.system(command)
command = "python heatmap.py --ytick 60s data"+now+".csv power"+now+".png"
print (time.strftime("%Y-%m-%d %H:%M:%S ") + command)
os.system(command)
os.system("mv power*.png ../Share/")
os.system("mv max*.png ../Share/")

# Repeat every hour
while True:

    # wait untill next hour
    print (time.strftime("%Y-%m-%d %H:%M:%S ") + "Wait untill next hour")
    while True:
        if int(time.strftime("%M"))==0:
            break
        time.sleep(1)

    now = time.strftime("_%Y%m%d_%H")
    command = "rtl_power -f 1415M:1425M:5k -i 10 -g 50 -c 0.40 -e 58m data"+now+".csv"
    print (time.strftime("%Y-%m-%d %H:%M:%S ") + command)
    os.system(command)
    command = "python heatmap.py --ytick 60s data"+now+".csv power"+now+".png"
    print (time.strftime("%Y-%m-%d %H:%M:%S ") + command)
    os.system(command)
    os.system("mv power*.png ../Share/")
    os.system("mv max*.png ../Share/")
    

