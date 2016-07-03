'''This Module is the main screen file.'''

#Imports
import os
from datetime import date

#Function to convert folder name into human readable format date
def conv_readdate(dt):
	dt_year = 2000+int(dt/1000)
	dt_doy = dt%1000
	t = date.fromordinal(date(dt_year, 1, 1).toordinal() + dt_doy - 1)
	return t

#Check latest date of the data available
os.chdir('/home/deathstroke/projects/IITI_GNSSR/data/')
sub = [x for x in os.listdir('.') if os.path.isdir(x)]
dt = max(sub)
date_upto = conv_readdate(int(dt))
os.chdir('/home/deathstroke/projects/IITI_GNSSR/iiti_gnssr/')


print ('''
	Select any one of the following options
----------------------------------------------------------
1. Plot cummulative graph of TEC vs time for all satellites of a given constellation for given dates
2. Plot cummulative graph of VTEC vs time for all satellites of a given constellation for given dates
3. Plot cummulative graph of Iono delay(in meters) Vs time for all satellites of a given constellation for given dates
4. Quit
'''
	)
print ("\nData available upto %s\n" %date_upto)

cnt = 0
while(cnt!=1):
	select = input("Enter your choice>> ")

	if select==1:
		cnt = 1
		import tecvtime
		tecvtime.main()
	elif select==2:
		cnt = 1
		import vtecvtime
		altvtecvtime.main()
	elif select==3:
		cnt = 1
		import ionodelayvtime
		ionodelayvtime.main()
	elif select==4:
		cnt = 1
		quit()
	else:
		print ("Please enter a valid choice!!!")

