import os
import time
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

prefix = '/media/michel/SETI/'
start_date = date(2016, 1, 1)
end_date = date(2020, 1, 1)
for single_date in daterange(start_date, end_date):
    os.system ('mkdir '+ prefix + single_date.strftime("%Y"))    
    os.system ('mkdir '+ prefix + single_date.strftime("%Y")+ '/' + single_date.strftime("%Y%m%d"))

