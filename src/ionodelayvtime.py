# Imports
import os,copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta as td

# Function to cheak if leap year
def checkleap(year):
	return ((year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)))

# Date of the year Conversion
def convert_date(day,month,year):
	if checkleap(year)==True:
		days = [31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
		if month == 1:
			return day
		else:
			return day+days[month-2]
	else:
		days = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
		if month == 1:
			return day
		else:
			return day+days[month-2]

#Function to check presence of Nan			
def checknonan(df):
	for i in df:
		if np.isnan(i):
			return False
	return True

#Function to count number of Nan	
def countnan(df):
	count = 0
	for i in df:
		if np.isnan(i):
			count = count+1
	return count

#Function to convet time of week in seconds to hours
def gettime(times):
	hours = 0.0
	minutes = 0.0
	t = -1
	tm = []
	for each in times:
		if t!=each:
			minutes = minutes+1
			if minutes>60:
				hours = hours+1
				minutes = minutes%60
			t = each
		tm1 = float(hours+(float(minutes/60)))
		tm.append(tm1)
	return tm

#Function to check validity of dates
def validdt(start_date,start_month,start_year,end_date,end_month,end_year,date_from,date_upto):
    if start_year>end_year or (start_year<date_from.year or end_year>date_upto.year) :
        return False
    elif start_year==end_year and (start_year==date_from.year and end_year==date_upto.year) and (start_month>end_month or start_month<date_from.month or end_month>date_upto.month):
        return False
    elif start_year==end_year and (start_year==date_from.year and end_year==date_upto.year) and start_month==end_month and (start_month==date_from.month and end_month==date_upto.month) and (start_date>end_date or start_date<date_from.day or end_date>date_upto.day):
        return False
    return True

#Function to obtain range of dates
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + td(n)

#Function to convert folder name into human readable format date
def conv_readdate(dt):
	dt_year = 2000+int(dt/1000)
	dt_doy = dt%1000
	t = date.fromordinal(date(dt_year, 1, 1).toordinal() + dt_doy - 1)
	return t

def main():
	#Check latest date of the data available
	os.chdir('/home/deathstroke/projects/IITI_GNSSR/data/')
	sub = [x for x in os.listdir('.') if os.path.isdir(x)]
	dt = max(sub)
	date_upto = conv_readdate(int(dt))
	os.chdir('/home/deathstroke/projects/IITI_GNSSR/iiti_gnssr/')
	#Check oldest date of the data available
	os.chdir('/home/deathstroke/projects/IITI_GNSSR/data/')
	sub = [x for x in os.listdir('.') if os.path.isdir(x)]
	dt = min(sub)
	date_from = conv_readdate(int(dt))
	os.chdir('/home/deathstroke/projects/IITI_GNSSR/iiti_gnssr/')
	print ("\nData available from %s to %s\n" %(date_from,date_upto))


	alpha=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']

	#Taking valid start and end dates as input from user
	validity = False
	while(validity!=True):
		start_date = int(input("Enter Start Date(dd):"))
		start_month = int(input("Enter Start Month(mm):"))
		start_year = int(input("Enter Start Year(yyyy):"))
		print ("\n")
		end_date = int(input("Enter End Date(dd):"))
		end_month = int(input("Enter End Month(mm):"))
		end_year = int(input("Enter End Year(yyyy):"))
		print ("\n")
		validity = validdt(start_date,start_month,start_year,end_date,end_month,end_year,date_from,date_upto)
		if validity == False:
			print ("\nPlease enter valid start and end dates\n")

	#Conversion into datetime format
	d1 = date(start_year,start_month,start_date)
	d2 = date(end_year,end_month,end_date+1)
	d3 = date(end_year,end_month,end_date)

	#Reading and storing data from different files
	frames = []
	for single_date in daterange(d1,d2):
		curr_date = str(convert_date(int(single_date.day),int(single_date.month),int(single_date.year)))
		curr_folder = str(str(int(single_date.year)%2000)+str(curr_date))
		for letter in alpha:
			try:
				filename = str('IITI'+curr_date+letter+'.'+'16_.ismr')
				with open('/home/deathstroke/projects/IITI_GNSSR/data/%s/%s' %(curr_folder,filename)) as f:
					df = pd.read_csv(f,usecols=[1,2,22],names=['time','svid','TEC'])
					frames.append(df)
			except (IOError):
				df1 = copy.deepcopy(frames[len(frames)-1])
				df1['time']=df['time']+3600
				tec = ['nan' for each in df1['time']]
				df1['TEC'] = tec
				frames.append(df1)
	result =pd.concat(frames)
	result['t-hrs'] = gettime(result['time'])
	dfm = result.groupby('svid')
	svid = set()
	for elements in result['svid']:
			svid.add(elements)
	svid1 = sorted(svid)

	cnt = 0
	while(cnt!=1):
		print (
	'''Choose the satellite constellation whose data is required:-
	1. GPS
	2. GLONASS
		'''
		)
		constl = int(input(">> "))

		if constl==1:
			for each in svid1:
				if each>37:
					svid.remove(each)
			svid2 = sorted(svid)
			n = 37
			constl = 'gps'
			cnt=1
		elif constl==2:
			for each in svid1:
				if each<38 or each>61:
					svid.remove(each)
			svid2 = sorted(svid)
			constl = 'glonass'
			n = 24
			cnt=1
		else:
			print ("\nPlease enter a valid input")

	#Calculating average data points for plotting
	sumtime = 0
	count = 0
	for each in svid2:
		dftemp = dfm.get_group(each)
		timedf = np.array(dftemp['time'])
		tecdf = np.array(dftemp['TEC'],dtype=float)
		sumtime = sumtime+(timedf.size-countnan(tecdf))
		count = count+1
	avg = sumtime/count
	val = avg


	#Counting the number of plots
	count = 0
	for each in svid2:
		dftemp = dfm.get_group(each)
		timedf = np.array(dftemp['t-hrs'])
		tecdf = np.array(dftemp['TEC'],dtype=float)
		delaydf = tecdf*0.1623 
		if timedf.size-countnan(delaydf)>val:
			count = count +1


	#Plotting each satellite with datapoints greater than average
	clr = iter(plt.cm.rainbow(np.linspace(0,1,count)))
	handles = []
	for each in svid2:
		dftemp = dfm.get_group(each)
		timedf = np.array(dftemp['t-hrs'])
		tecdf = np.array(dftemp['TEC'],dtype=float)
		delaydf = tecdf*0.1623
		if timedf.size-countnan(delaydf)>val:
			cl = next(clr)
			plt.plot(timedf,delaydf,label='%d' %each,c=cl)
			handles.append(str(each))

	# Ensure that the axis ticks only show up on the bottom and left of the plot.  
	# Ticks on the right and top of the plot are generally unnecessary chartjunk.  
	ax = plt.subplot(111)    
	ax.spines["top"].set_visible(False)    
	# ax.spines["bottom"].set_visible(False)    
	ax.spines["right"].set_visible(False)    
	# ax.spines["left"].set_visible(False)

	# Ensure that the axis ticks only show up on the bottom and left of the plot.  
	# Ticks on the right and top of the plot are generally unnecessary chartjunk.  
	ax.get_xaxis().tick_bottom()  
	ax.get_yaxis().tick_left()

	plt.xlabel('Time in hours(0 is 5:30 AM IST on %s)' %d1)
	plt.ylabel('Iono-delay in metres for L1 band')
	plt.title('Iono-delay claculated from TEC data collected from %s constellation for %s to %s \nShowing satellites with %d+ datapoints' %(constl.upper(),d1,d3,val))
	plt.legend(bbox_to_anchor=(1, 1), loc='upper left',prop={'size':12}, borderaxespad=0.,frameon=False)
	plt.show()

if __name__=="__main__":
	main()
