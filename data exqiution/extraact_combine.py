# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 16:32:00 2020

@author: ASUS
"""

from plot_aqi import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv

def met_data(month,year):
    file_html =open('Data/html_data/{}/{}.html'.format(year, month),'rb')
    plain_text=file_html.read()
    
    tempD=[]
    finalD=[]
    
    soup= BeautifulSoup(plain_text,'lxml')
    
    for table in soup.findAll('table',{'class':'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a=tr.get_text()
                tempD.append(a)
    
    #we will get all rows in one single list so we have to divide to according to features
    #that way we can get total rows               
    rows=len(tempD)/15
    
    for times in range(round(rows)):
        newtempD=[]
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        # one-one row will be added to finalD    
        finalD.append(newtempD)
    
    
    length= len(finalD)
    
    #this row is description so we dont need it
    finalD.pop(length-1)
    
    #this row is feature name row because we deleting some features so we r deleting right now for simplicity
    finalD.pop(0)
    
    
    for a in range(len(finalD)):
        #they are some unnecessary columns so we r deleting from every cell
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)
        
    return finalD
#lets combine our csv file to one major file
def data_combine(year,chunk_size):
    for i in pd.read_csv('Data/Real-Data/real_'+str(year)+'.csv',chunksize=chunk_size):
        df=pd.DataFrame(data=i)
        mylist=df.values.tolist()
    
    return mylist


if __name__=='__main__' :
    if not os.path.exists('Data/Real-Data'):
        os.makedirs('Data/Real-Data')
    for year in range(2013,2017):
        final_data=[]
        with open('Data/Real-Data/real_'+str(year)+'.csv','w') as csvfile:
            #making csv file
            wr =csv.writer(csvfile, dialect='excel')
            #first row 
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        #now first row is written now we r going to add whole year data for that we have to make it
        for month in range(1,13):
            #it will also give me rows of list
            temp=met_data(month, year)
            #this we are adding to whole database like rows in one list
            final_data=final_data+temp
            
        # callig our pm values by the mmethods in plot_aqi
        pm=getattr(sys.modules[__name__], 'avg_data_{}'.format(year))()
        
        if len(pm)==364:
            #last 365 place 
            pm.insert(364,'-')
        #here we have whole data of 2013
        
        for i in range(len(final_data)-1):
            #adding our output variable 
            final_data[i].insert(8,pm[i])
            
        #here we are appending before we only write
        with open('Data/Real-Data/real_'+str(year)+'.csv','a') as csvfile:
                       
            #same as we have done in row 72.
            wr=csv.writer(csvfile,dialect='excel')
            for row in final_data:
                flag = 0
                for element in row:
                    #means if we have null value in one row we will not take that row
                    if element == '' or element == '-':
                        flag=1
                if flag != 1:
                    wr.writerow(row)
    
            print('done')
             
    data_2013=data_combine(2013, 600)
    data_2014=data_combine(2014, 600)
    data_2015=data_combine(2015, 600)
    data_2016=data_combine(2016, 600)

    total_data = data_2013+data_2014+data_2015+data_2016            
    
    with open('Data/Real-Data/Real_Combine.csv','w') as csvfile:
            wr =csv.writer(csvfile, dialect='excel')
            #first row 
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
            wr.writerows(total_data)
        
    
    
    df=pd.read_csv('Data/Real-Data/Real_Combine.csv')
    
    
    
    
    
    
    
        