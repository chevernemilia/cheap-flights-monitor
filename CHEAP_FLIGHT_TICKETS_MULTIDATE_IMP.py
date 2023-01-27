#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# this is a demo study to learn from how to do data crawling for flight ticket check
# demo study from :https://medium.com/@fneves/if-you-like-to-travel-let-python-help-you-scrape-the-best-fares-5a1f26213086


# In[1]:


from IPython.core.display import display, HTML
import pandas as pd
# use below to widen the notebook cells, helpfulf or coding & viz
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option("display.max_rows", None, "display.max_columns", None)


# In[2]:


# package location: /Users/eli/eli_venv/lib/python3.7/site-packages

import numpy as np  
import sys
import math
import matplotlib.pyplot as plt
import os
import seaborn as sns
import time

# from time import sleep, strftime

# from random import randint
import pandas as pd
import sys
# still need to figure how to permanently add directory to pythonpath
sys.path.append('/Users/eli/eli_venv/lib/python3.7/site-packages')

import smtplib
from email.mime.multipart import MIMEMultipart
import re
import itertools

import datetime 
# current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

current_datetime

from fpdf import FPDF
from PIL import Image
import glob
import os
from os.path import exists

# this need to use the module as prefix each time using the func of the module
# import  cft_modules as cft
# this skip the prefix from module name each time calling the module func
from  cft_modules import *


# fig, ax = plt.subplots(figsize=(10,5))


# ## Create .pdf & .txt file and write all key plots and df accordingly

# In[3]:


# this step tries to set up all files with their absolute dir, set up first so info.log can be writtened
#################################### create new files and locate them ######################################################
# current timestamp include hours and minutes
# current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
script_start_time = time.time()

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")

output_dir = '/Users/eli/Python/personal_projects/CheapFlightTickets/analysisResultOutput/'
os.chdir(output_dir)


output_pdf = output_dir + 'CheapFlightTicket_MultipleDates-' + current_date + '.pdf'
output_txt = output_dir + 'CheapFlightTicket_MultipleDates-' + current_date + '.txt'
output_xlsx = output_dir + 'CheapFlightTicket_MultipleDates-' + current_date + '.xlsx'

#################################### convert key df into .txt file ######################################################
# if txt file (output_txt) with exact same name (very unlikely due to hour/min label) exist, then clear and rewrite on it
# for now only keep the file name tag up to date, not time
if exists(output_txt):
    with open (output_txt, 'r+') as f:
        f.truncate(0)  

# turn the df into .txt file in specific dir defined prior   
# not do this step as excel file do better job to keep and display flight records
# let's use the csv/txt/log txt fille as script-run info log file
# with open(output_txt, 'a') as f:
#     df_as_string = cheap_flight_round_trip.to_string(header=False, index=False)
#     f.write(df_as_string)
# f.close()
tfile = open(output_txt, 'a')


# In[4]:


# current_datetime
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d: %H:%M %p")

tstring = 'Date & Time for Flights Inquiry: ' + current_datetime
print(tstring)
tfile.write(tstring)
tfile.write('\n\n')


# In[5]:


# change dir for images/charts that will be created & stored after web data quiry, clean and eval
os.chdir('/Users/eli/Python/personal_projects/CheapFlightTickets/outputImages')


# In[6]:



# chromedriver-path: /home/eli/eli_env/bin/chromedriver-path
# # chromedriver location:
# #  chromedriver -v
# # ChromeDriver 104.0.5112.79 (3cf3e8c8a07d104b9e1260c910efb8f383285dc5-refs/branch-heads/5112@{#1307})
# make sure chrome version and chrome driver version are compatible; eg: if chrome version is 108 then chrome driver need to be update to 108 as well
# the observation is that chrome version got update every every month 
# (107 on 10/25/2022, 108 on 11/30/2022, 106 on 9/28/2022, 109 on 1/24/2023)
# check the Google Chrome version by typing in browser: chrome://version/  check first line
# download the appropriate chrome driver and bring to your destinated chromedriver_path
# tell MacOS to trust this binary: xattr -d com.apple.quarantine /Users/eli/eli_venv/lib/python3.7/site-packages/chromedriver
# detech to see if system recognize chromedriver in the system by using which chromedriver, 
# if not need to set the path of chromedriver as system env var in .bashrc/.bash_profile
# need to refressh sys env var by doing: source ~/.bashrc or source ~/.bash_profile
# if error persist try to restart the machine

# chromedriver_path = '/Users/eli/eli_venv/lib/python3.7/site-packages/chromedriver'

# a new window would pop up
# driver = webdriver.Chrome(executable_path=chromedriver_path) # This will open the Chrome window

chromedriver_path = '/Users/eli/eli_venv/lib/python3.7/site-packages/chromedriver'
# chromedriver_path = '/Users/eli/eli_venv/lib/python3.7/site-packages/chromedriver_mac64'


chromedriver_path

driver = webdriver.Chrome(executable_path=chromedriver_path) # This will open the Chrome window instance

# driver = webdriver.Chrome(executable_path=chromedriver_path, service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get()

# options = webdriver.ChromeOptions()
# options.add_argument("--no-sandbox")
# options.add_argument("--remote-debugging-port=9222")
# options.headless = True

# driver = webdriver.Chrome(executable_path=chromedriver_path, options = chrome_options) # This will open the Chrome window

sleep(2)
driver.maximize_window() # For maximizing window
# driver.implicitly_wait(20) # gives an implicit wait for 20 seconds


# # Config for Single Destination On Multiple Flight Dates

# In[7]:


city_from = 'SFO'

city_to = 'LHR' #England, London 

# flight_date = ['2023-05-03', '2023-05-10', '2023-05-17', '2023-05-24']

flight_date = ['2023-05-03', '2023-05-10']


# flight_date = ['2023-01-10', '2023-01-17', '2023-01-24',
#                '2023-02-03', '2023-02-10', '2023-02-17', '2023-02-24',
#                '2023-03-03', '2023-03-10', '2023-03-17', '2023-03-24',
#                '2023-04-03', '2023-04-10', '2023-04-17', '2023-04-24',
#                '2023-05-03', '2023-05-10', '2023-05-17', '2023-05-24',
#                '2023-06-03', '2023-06-10', '2023-06-17', '2023-06-24',
#               '2023-07-03', '2023-07-10', '2023-07-17', '2023-07-24',
#               '2023-08-03', '2023-08-10', '2023-08-17', '2023-08-24',
#               '2023-09-03', '2023-09-10', '2023-09-17', '2023-09-24',
#               '2023-10-03', '2023-10-10', '2023-10-17', '2023-10-24']

# flight_date = ['2023-10-03', '2023-10-10', '2023-10-17', '2023-10-24']

# depends on the capability of date range your selected search engine can provide, for Kayak, nbr_dt_range_search <=3, any int more still <= 3, 
# so that means max could search for 7 days in kayak: exact day +/-3days, which is a range in a week
# nbr_dt_range_search = 1 means could be +/-1 day
nbr_dt_range_search = 3
# nbr_click_this_session = 3 # additional click after each initiate browsing so nbr of list is n+1
nbr_click_this_session = 1 # additional click after each initiate browsing so nbr of list is n+1

tstring = 'city_from: '+ city_from
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'city_to: ' + city_to
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'flight_date: ' + str(flight_date)
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'nbr_dt_range_search: ' + str(nbr_dt_range_search)
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'nbr_click_this_session: ' + str(nbr_click_this_session)
print(tstring)
tfile.write(tstring)
tfile.write('\n\n')

depart_destinations = "-".join([city_from,city_to ])
depart_destinations


# ## Iterate Search Flights Same Location at Different Time Range 
# ### Could be a full month when nbr_dt_range_search is x+/-3d as in a week for 4 diff x values

# In[8]:


# create empty df so each forloop sub_df can be add into master df
cheap_flight_master = pd.DataFrame()
# get info of the dt for which current sessions of queries starts, assuming price changes at anytime based on date & time of query
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M %p")
tstring = 'Current Time To Search Flights: ' +  current_datetime
print(tstring)
tfile.write(tstring)
tfile.write('\n')

master_start_time = time.time()

for date in flight_date:
    
    cheap_flights = get_cheap_flights(city_from, city_to, date, nbr_dt_range_search, nbr_click_this_session)
    
    if (cheap_flights is not None):

        print("nbr of cheap_flights in this search on: ", date, " is ", cheap_flights.shape[0])
        print('------------------------------------------------------------------------------------------------\n')
        print('\n')
    #     continuously add cheap_flights df into cheap_flight_master df, rbind
        cheap_flight_master = cheap_flight_master.append(cheap_flights)

# create a new df called: cheap_flight_master_depart 
cheap_flight_master_depart = cheap_flight_master

cheap_flight_master.shape


tstring = "Nbr of cheap flights in this search: " + str(cheap_flight_master.shape[0])
print(tstring)
tfile.write(tstring)
tfile.write('\n')

tstring = "--- %s mintues " % float( '%.5g' % ((time.time() - master_start_time)/60)) + 'to complete this seach session. --------'
print(tstring)
tfile.write(tstring)
tfile.write('\n\n')


# # Visualization

# ## Top 10 Lowest Price Flight in Current Search:

# In[9]:


print("Here's the Top 10 Lowest Flight Price In Current Search:\n")
cheap_flight_master.sort_values(by = 'lowest_price', inplace = True)
cheap_flight_master.head(10)


# ## Display Lowest Flight Price In A Time Range

# In[10]:


cheap_flight_master = cheap_flight_master_depart


# In[11]:


plt.rcParams["figure.figsize"] = (10,4)
# plt.figure(figsize=(10,4)) 

cheap_flight_master.sort_values(by = 'date', inplace = True)

title_string = "Lowest Flight Prices In a Day Range to " +  city_to

plot = sns.catplot(
    data=cheap_flight_master, 
    kind="box",
    x="date", 
    y="lowest_price",
    height=5, aspect=3, 
    legend = True,
).set(title = title_string)

plt.savefig('Img01.jpg', bbox_inches = 'tight')

# plt.show()

plt.rcParams["figure.figsize"] = (10,4)


title_string = "Lowest Flight Prices In a Day Range Distributed by Nbr Stops to " +  city_to
sns.catplot(
    data=cheap_flight_master, 
    kind="box",
    x="date", 
    y="lowest_price",
    hue="nbr_stop",
#     ax = axs,
    height=5, aspect=3
#     errorbar="sd", palette="dark", alpha=.6, height=6
).set(title = title_string)

plt.savefig('Img02.jpg', bbox_inches = 'tight')
# plt.savefig('Img02.jpg', bbox_inches = 'tight', dpi = 150)

# plt.show()



# In[12]:


plt.rcParams["figure.figsize"] = (10,4)

print('Lowest Price & Flight Hours Distribution:')
cheap_flight_master[['lowest_price', 'flight_hr']].hist(bins = 50)
plt.savefig('Img03.jpg', bbox_inches = 'tight')

# plt.show()
# plt.title(['Flight Amount in: ' + df_avaialable_dt[0], 'Flight Amount in: ' + df_avaialable_dt[0]])
five_pt_stats = cheap_flight_master[['lowest_price', 'flight_hr']].describe()
five_pt_stats = five_pt_stats.round(2).reset_index()

five_pt_stats

title_string = "Statistcs of Flight Info to " +  city_to
render_mpl_table(five_pt_stats, header_columns=2, col_width=2,  row_height=0.5,  font_size=12)
plt.title(title_string)
plt.savefig('Img04.jpg', bbox_inches = 'tight')
# plt.show()


# # Multiple Flight Dates Features Correlation

# In[13]:


cheap_flight_master.head()


# In[14]:


plt.rcParams["figure.figsize"] = (8,5)

sns.relplot(data=cheap_flight_master, x="lowest_price", y="flight_hr", 
            hue="date", 
#             hue="nbr_stop", 
#             legend = False
           )
plt.title('lowest_price vs. flight_hr')
# plt.legend(ncol = 3, loc = 'best', bbox_to_anchor=(0, 1))
# plt.savefig('Img05.jpg', bbox_inches = 'tight')
# plt.show()

sns.relplot(data=cheap_flight_master, x="lowest_price", y="flight_hr", 
            hue="date", 
#             col="nbr_stop"
           )
# plt.title('lowest_price vs. flight_hr')
# plt.savefig('Img06.jpg', bbox_inches = 'tight')
# plt.show()

plt.rcParams["figure.figsize"] = (8,8)

sns.relplot(data=cheap_flight_master, x="lowest_price", y="flight_hr", 
            hue="nbr_stop", 
            col="checked_bag"
           )
plt.savefig('Img07.jpg', bbox_inches = 'tight')
# plt.show()

plt.rcParams["figure.figsize"] = (8,8)

sns.relplot(data=cheap_flight_master, x="lowest_price", y="flight_hr", 
            hue="nbr_stop", 
            col="carry_on_bag"
           )
plt.savefig('Img08.jpg', bbox_inches = 'tight')
# plt.show()


# ## Flight Frequency Available In Search By Datetime
# ### more applicable for few flight destinations

# In[15]:


plt.rcParams["figure.figsize"] = (10,25)

# flight_time_stats = cheap_flight_master['time'].value_counts().reset_index().rename(columns ={'index':'time', 'time': 'nbr_flights'} )

cheap_flight_master= cheap_flight_master.sort_values(by = 'date')
flight_time_stats = cheap_flight_master.groupby(['date','datetime', 'nbr_stop'])['time'].count().reset_index().rename(columns = {'time':'nbr_flight'})

flight_time_stats
sns.barplot(data=flight_time_stats, 
            x="nbr_flight",
            y="datetime",
            hue = 'nbr_stop',
           )
plt.title('Flight Frequency By Datetime')
# plt.show()


# In[16]:


city_from = 'CDG'  #France
city_to = 'SFO' #England, London 

# date must be aligned with current search engine web date info: Kayak: yyyy-mm-dd
# flight_date = ['2023-05-10', '2023-05-17', '2023-05-24','2023-06-03']

flight_date = [ '2023-05-24','2023-06-03']


# flight_date = ['2023-01-10', '2023-01-17', '2023-01-24',
#                '2023-02-03', '2023-02-10', '2023-02-17', '2023-02-24',
#                '2023-03-03', '2023-03-10', '2023-03-17', '2023-03-24',
#                '2023-04-03', '2023-04-10', '2023-04-17', '2023-04-24',
#                '2023-05-03', '2023-05-10', '2023-05-17', '2023-05-24',
#                '2023-06-03', '2023-06-10', '2023-06-17', '2023-06-24',
#               '2023-07-03', '2023-07-10', '2023-07-17', '2023-07-24',
#               '2023-08-03', '2023-08-10', '2023-08-17', '2023-08-24',
#               '2023-09-03', '2023-09-10', '2023-09-17', '2023-09-24',
#               '2023-10-03', '2023-10-10', '2023-10-17', '2023-10-24']

# flight_date = [ '2023-05-24',
#                '2023-06-03', '2023-06-10', '2023-06-17', '2023-06-24',
#               '2023-07-03', '2023-07-10', '2023-07-17', '2023-07-24',
#               '2023-08-03', '2023-08-10', '2023-08-17', '2023-08-24',
#               '2023-09-03', '2023-09-10', '2023-09-17', '2023-09-24',
#               '2023-10-03', '2023-10-10', '2023-10-17', '2023-10-24']

# depends on the capability of date range your selected search engine can provide, for Kayak, nbr_dt_range_search <=3, any int more still <= 3, 
# so that means max could search for 7 days in kayak: exact day +/-3days, which is a range in a week
# nbr_dt_range_search = 1 means could be +/-1 day
nbr_dt_range_search = 3
# nbr_click_this_session = 3
nbr_click_this_session = 1 # additional click after each initiate browsing so nbr of list is n+1

tstring = 'city_from: '+ city_from
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'city_to: ' + city_to
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'flight_date: ' + str(flight_date)
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'nbr_dt_range_search: ' + str(nbr_dt_range_search)
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'nbr_click_this_session: ' + str(nbr_click_this_session)
print(tstring)
tfile.write(tstring)
tfile.write('\n')


return_destinations = "-".join([city_from,city_to ])
return_destinations


# In[17]:


# create empty df so each forloop sub_df can be add into master df
cheap_flight_master = pd.DataFrame()
# get info of the dt for which current sessions of queries starts, assuming price changes at anytime based on date & time of query
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print('Current Time To Search Flights:', current_datetime)

master_start_time = time.time()

for date in flight_date:
    
    cheap_flights = get_cheap_flights(city_from, city_to, date, nbr_dt_range_search, nbr_click_this_session)
    
    if (cheap_flights is not None):

        print("nbr of cheap_flights in this search on: ", date, " is ", cheap_flights.shape[0])
        print('------------------------------------------------------------------------------------------------\n')
        print('\n')
    #     continuously add cheap_flights df into cheap_flight_master df, rbind
        cheap_flight_master = cheap_flight_master.append(cheap_flights)

cheap_flight_master_return = cheap_flight_master

tstring = "Nbr of cheap flights in this search: " + str(cheap_flight_master.shape[0])
print(tstring)
tfile.write(tstring)
tfile.write('\n')

tstring = "--- %s mintues " % float( '%.5g' % ((time.time() - master_start_time)/60)) + 'to complete this seach session. --------'
print(tstring)
tfile.write(tstring)
tfile.write('\n\n')


cheap_flight_master.shape


# In[18]:


cheap_flight_master = cheap_flight_master_return


# In[19]:



cheap_flight_master.sort_values(by = 'date', inplace = True)

title_string = "Lowest Flight Prices In a Day Range to " +  city_to

plot = sns.catplot(
    data=cheap_flight_master, 
    kind="box",
    x="date", 
    y="lowest_price",
    height=5, aspect=3, 
    legend = True,
).set(title = title_string)

plt.savefig('Img09.jpg', bbox_inches = 'tight')

# plt./show()

title_string = "Lowest Flight Prices In a Day Range Distributed by Nbr Stops to " +  city_to
sns.catplot(
    data=cheap_flight_master, 
    kind="box",
    x="date", 
    y="lowest_price",
    hue="nbr_stop",
#     ax = axs,
    height=5, aspect=3
#     errorbar="sd", palette="dark", alpha=.6, height=6
).set(title = title_string)

plt.savefig('Img10.jpg', bbox_inches = 'tight')
# plt.savefig('Img02.jpg', bbox_inches = 'tight', dpi = 150)

# plt.show()



# In[20]:


plt.rcParams["figure.figsize"] = (10,4)

print('Lowest Price & Flight Hours Distribution:')
cheap_flight_master[['lowest_price', 'flight_hr']].hist(bins = 50)
plt.savefig('Img11.jpg', bbox_inches = 'tight')
# plt.show()

# plt.title(['Flight Amount in: ' + df_avaialable_dt[0], 'Flight Amount in: ' + df_avaialable_dt[0]])
five_pt_stats = cheap_flight_master[['lowest_price', 'flight_hr']].describe()
five_pt_stats = five_pt_stats.round(2).reset_index()

five_pt_stats

title_string = "Statistcs of Flight Info to " +  city_to
render_mpl_table(five_pt_stats, header_columns=2, col_width=2,  row_height=0.5,  font_size=12)
plt.title(title_string)
plt.savefig('Img12.jpg', bbox_inches = 'tight')
# plt.show()


# In[21]:


plt.rcParams["figure.figsize"] = (5,5)

sns.relplot(data=cheap_flight_master, x="lowest_price", y="flight_hr", 
            hue="date", 
           )
plt.title('lowest_price vs. flight_hr')
# plt.savefig('Img13.jpg', bbox_inches = 'tight')
# plt.show()

sns.relplot(data=cheap_flight_master, x="lowest_price", y="flight_hr", 
            hue="date", 
            col="nbr_stop"
           )
# plt.title('lowest_price vs. flight_hr')
# plt.savefig('Img14.jpg', bbox_inches = 'tight')
# plt.show()

plt.rcParams["figure.figsize"] = (8,8)

sns.relplot(data=cheap_flight_master, x="lowest_price", y="flight_hr", 
            hue="nbr_stop", 
            col="checked_bag"
           )
plt.savefig('Img15.jpg', bbox_inches = 'tight')
# plt.show()

plt.rcParams["figure.figsize"] = (8,8)

sns.relplot(data=cheap_flight_master, x="lowest_price", y="flight_hr", 
            hue="nbr_stop", 
            col="carry_on_bag"
           )
plt.savefig('Img16.jpg', bbox_inches = 'tight')
# plt.show()


# ## Merge cheap_flight_master_go & cheap_flight_master_back (Multiple Date Choices On Target Locations)

# In[22]:



# get mean & median of each variable
price_threshold_depart = round(min(cheap_flight_master_depart['lowest_price'].describe()[[1,5]].tolist()),2)
price_threshold_depart

flight_hr_threshold_depart = round(min(cheap_flight_master_depart['flight_hr'].describe()[[1,5]].tolist()),2)
flight_hr_threshold_depart

price_threshold_return = round(min(cheap_flight_master_return['lowest_price'].describe()[[1,5]].tolist()))
price_threshold_return

flight_hr_threshold_return = round(min(cheap_flight_master_return['flight_hr'].describe()[[1,5]].tolist()),2)
flight_hr_threshold_return


tstring = 'price_threshold_depart: ' + str(price_threshold_depart)
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'flight_hr_threshold_depart: ' + str(flight_hr_threshold_depart)
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'price_threshold_return: ' + str(price_threshold_return)
print(tstring)
tfile.write(tstring)
tfile.write('\n')
tstring = 'flight_hr_threshold_return: ' + str(flight_hr_threshold_return)
print(tstring)
tfile.write(tstring)
tfile.write('\n')


trip_duration_threshold = [5, 14]


# In[23]:


cheap_flight_master_depart['flight_hr'].describe()


# In[24]:


# add prefix so you two df of diff purposes can be differentiated after merged
cheap_flight_master_go = cheap_flight_master_depart.add_prefix('g_')
cheap_flight_master_back = cheap_flight_master_return.add_prefix('b_')

print('cheap_flight_master_go: ', cheap_flight_master_go.shape)
print('cheap_flight_master_back: ', cheap_flight_master_back.shape)



################################################################################################
# This is optional to filter cheaper price or less flight hours 
# remove outside budget flights to expedite merging for interested of flights, not going to pick high end
cheap_flight_master_go = cheap_flight_master_go[(cheap_flight_master_go['g_flight_hr']<= flight_hr_threshold_depart)  | (cheap_flight_master_go['g_lowest_price']<= price_threshold_depart)]
cheap_flight_master_back = cheap_flight_master_back[(cheap_flight_master_back['b_flight_hr']<=flight_hr_threshold_return)  & (cheap_flight_master_back['b_lowest_price']<= price_threshold_return)]
################################################################################################

print('cheap_flight_master_go: ', cheap_flight_master_go.shape)
print('cheap_flight_master_back: ', cheap_flight_master_back.shape)


# the col/idx to merge from, here we want to have single from/to which is sfo for now
cheap_flight_round_trip = pd.merge(cheap_flight_master_go, cheap_flight_master_back, left_on = 'g_from' , right_on = 'b_to')
# cheap_flight_round_trip = pd.merge(cheap_flight_master_go, cheap_flight_master_back)

print('cheap_flight_round_trip: ', cheap_flight_round_trip.shape)

cheap_flight_round_trip.drop_duplicates(inplace = True)
print('cheap_flight_round_trip: ', cheap_flight_round_trip.shape)

from datetime import datetime
# get current year to fill out the full date info from the df
current_yr = datetime.today().strftime("%Y")
# convert date in string to datetime to cal for trip duration/
cheap_flight_round_trip['g_dt_str'] = [x + '/' +(current_yr) for x in cheap_flight_round_trip['g_date']]
cheap_flight_round_trip['g_dt'] = [datetime.strptime(x, '%m/%d/%Y' ) for x in cheap_flight_round_trip['g_dt_str']]
cheap_flight_round_trip['b_dt_str'] = [x + '/' +(current_yr) for x in cheap_flight_round_trip['b_date']]
cheap_flight_round_trip['b_dt'] = [datetime.strptime(x, '%m/%d/%Y' ) for x in cheap_flight_round_trip['b_dt_str']]
# substraction get timedelta obj which is converted into int
cheap_flight_round_trip['trip_duration_dt'] = (cheap_flight_round_trip['b_dt'] - cheap_flight_round_trip['g_dt']).dt.days
cheap_flight_round_trip= cheap_flight_round_trip[cheap_flight_round_trip['trip_duration_dt']>  0]
# cheap_flight_round_trip[['g_date', 'g_dt_str', 'g_dt', 'b_date','b_dt_str', 'b_dt','trip_duration' ]]
# cheap_flight_round_trip[['g_dt', 'b_dt','trip_duration' ]]


# get more stats for the terminal flights total price & flight hours, and intermediate travel IATA
cheap_flight_round_trip['itm_travel'] = cheap_flight_round_trip['g_to'] + "-" + cheap_flight_round_trip['b_from']
cheap_flight_round_trip['rt_lowest_price'] = cheap_flight_round_trip['g_lowest_price'] + cheap_flight_round_trip['b_lowest_price']
cheap_flight_round_trip['rt_flight_hr'] = round(cheap_flight_round_trip['g_flight_hr'] + cheap_flight_round_trip['b_flight_hr'],2)
cheap_flight_round_trip.shape

print('cheap_flight_round_trip: ', cheap_flight_round_trip.shape)

# make sure g_to IATA is not the same as b_from IATA so we ensure multiple travel locationss (can deal with the intermediate flight later)
cheap_flight_round_trip = cheap_flight_round_trip[(cheap_flight_round_trip['g_to'] != cheap_flight_round_trip['b_from'])]
# ensure round trip contains certain days duration predefined:
cheap_flight_round_trip = cheap_flight_round_trip[cheap_flight_round_trip['trip_duration_dt'].between(min(trip_duration_threshold), max(trip_duration_threshold))]

cheap_flight_round_trip.drop_duplicates(inplace = True)

print('cheap_flight_round_trip: ', cheap_flight_round_trip.shape)

cheap_flight_round_trip.sort_values(by = 'rt_lowest_price', inplace = True)


tstring = 'trip_duration_threshold: ' + str(trip_duration_threshold)
print(tstring)
tfile.write(tstring)
tfile.write('\n')

tstring = 'Best round-trip flights filtered: ' + str(cheap_flight_round_trip.shape[0])
print(tstring)
tfile.write(tstring)
tfile.write('\n\n')


# In[25]:


plt.rcParams["figure.figsize"] = (8,8)

cheap_flight_round_trip['trip_duration_str'] = cheap_flight_round_trip['trip_duration_dt'].astype(str)
sns.relplot(data=cheap_flight_round_trip, x="rt_lowest_price", y="rt_flight_hr", 
            hue="trip_duration_str", 
           )
plt.title('Round Trip lowest_price vs. flight_hr')
plt.savefig('Img17.jpg', bbox_inches = 'tight')

# plt.show()


# In[26]:


# decide the columns to export
cheap_flight_rt_export = cheap_flight_round_trip[['g_date', 'g_time', 'g_airline', 'g_nbr_stop', 'g_intermediate_stop',
       'g_duration', 'g_from', 'g_to', 'g_checked_bag', 'g_carry_on_bag',
        'g_lowest_price',
       'g_flight_hr', 'g_datetime', 'b_date', 'b_time', 'b_airline',
       'b_nbr_stop', 'b_intermediate_stop', 'b_duration', 'b_from', 'b_to',
       'b_checked_bag', 'b_carry_on_bag','b_lowest_price', 'b_flight_hr', 'b_datetime', 
        'trip_duration_dt', 'itm_travel',
       'rt_lowest_price', 'rt_flight_hr', ]]


# In[27]:


title_string = "Cheap Flight Round Trip Info." 

chosen_cols = ['g_date', 'g_airline', 'g_nbr_stop', 'g_intermediate_stop',
        'g_from', 'g_to', 'g_lowest_price',
       'g_flight_hr', 'b_date',  'b_airline',
       'b_nbr_stop', 'b_intermediate_stop',  'b_from', 'b_to',
        'b_lowest_price', 'b_flight_hr',  'itm_travel',
       'rt_lowest_price', 'rt_flight_hr','trip_duration_dt']
cheap_flight_rt_display = cheap_flight_round_trip[chosen_cols].head(10)
cheap_flight_rt_display

render_mpl_table(cheap_flight_rt_display, header_columns=2, col_width=2,  row_height=0.5,  font_size=12)
plt.title(title_string)
plt.savefig('Img18.jpg', bbox_inches = 'tight')
# plt.show()


# ## Create Excel File for detailed Flight Record Info.

# In[47]:




#################################### convert key df into .xlsx file ######################################################
# convert detailed df into excel in current dir
cheap_flight_rt_export.to_excel(output_xlsx, index = False)


# In[29]:


############################### convert a list of images (.gif, .jpg, .png) of the same dir into a .pdf file.  ##########################
from fpdf import FPDF
from PIL import Image
import glob
import os

originalWidth = []
originalHeight = []
originalWidth = []
originalHeight = []

#define location of the images saved that you want to create a pdf report from
# usually is the same dir of the images just saved from this script, 
image_directory = '/Users/eli/Python/personal_projects/CheapFlightTickets/outputImages'
extensions = ('*.png', '*.jpg', '*.gif')

# create two objs one for each PS/DS team pdf report output
pdf = FPDF()

imagelist = []

for ext in extensions: 
    imagelist.extend(glob.glob(os.path.join(image_directory, ext)))
    
imagelist = sorted(imagelist)
imagelist

accum_height = 0
orientation = 'L'
pdf.add_page(orientation=orientation)


# for imageFile in imagelist:
for idx, imageFile in enumerate(imagelist):
    print('idx:', idx)
    cover = Image.open(imageFile)
    width, height = cover.size
#     print('\n')
    print(imageFile)
    
    print('original width',width, ":",'original height', height)
    print('initial area:', width*height )
    print('width / height:', round(width / height) )

    x,y = 20,20
    #customized resize the original image size based on h & w ratio & width conditions, 
#     x, y are for the page margin to put the image 
#     choice are the marker to track label during development
    if (round(width / height) >= 3):
        
        if(width < 2000):
            width, height = round(float(width * 0.15)),  round(float(height * 0.15))
            x,y = 20,20
            choice = 1.1
        
        else:
            width, height =  round(float(width * 0.085)),  round(float(height * 0.11))
            x,y = 12,20
            choice = 1.2

    elif (round(width / height) >= 2):
        if(width >= 1300):
            width, height =  round(float(width * 0.4)),  round(float(height * 0.4))
            x,y = 20,20
            choice = 2.1

        else:
            width, height =  round(float(width * 0.16)),  round(float(height * 0.16))
            x,y = 60,20
            choice = 2.2

        
    else: 
        width, height =  round(float(width * 0.15)),  round(float(height * 0.15))
        x,y = 80,20
        choice = 3


#     orientatation of the page depend on the shape of the image
    pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

    # get page orientation from image size 
#     orientation = 'L'
#     print('orientation:', orientation)
    #  make sure image size is not greater than the pdf format size
    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

    print('adjusted size:',width,  height)
    print("accum_height before:", accum_height)
    
    if  accum_height>= 150:
        pdf.add_page(orientation=orientation)
        pdf.image(imageFile, x, y, width, height)
        accum_height = 0
        print('CHOICE:', choice)
        print('on NEW page')

    print('current y:', y)
    
    print('y', y)
    print('height', height)

    pdf.image(imageFile, x, accum_height+ y, width, height)
    print('on EXISTING page')
    print('CHOICE:', choice)

    accum_height += height + y

print(output_pdf)
pdf.output(output_pdf, "F")


# ## Indicate all flies location & close log files 

# In[30]:



tstring = 'Files Locations:\n'
# location of pdf
tfile.write(tstring)
tfile.write(output_pdf)
tfile.write('\n')
# location of xlsx
tstring = output_dir + output_xlsx
tfile.write(tstring)
tfile.write('\n')
# location of txt/log
tstring = output_txt
tfile.write(output_txt)
tfile.write('\n\n')

tstring = "--- %s mintues " % float( '%.5g' % ((time.time() - script_start_time)/60)) + 'to complete this script run. --------'
print(tstring)
tfile.write(tstring)
tfile.write('\n\n')


tfile.close()


# # Send Major Files To Target Emails

# In[34]:



################## Define all necesary elements for email #############
# subject = "ECL Email Test"
subject = "ECL Email Test: " + " " + depart_destinations  + "--" + return_destinations
# body = "Testing to see if target account receive email"
# body = "Testing to see if target accounts receive email w/ PDF & EXCEL Attachments, multiple emails, multile domains"
body = """Testing to see if target accounts receive email w/ PDF, EXCEL & TXT Attachments, multiple emails\n
DEPART DESTINATION:  """ + depart_destinations +"""\nRETURN DESTINATION:  """ + return_destinations

# sender = "aidatasciences@gmail.com"

sys.path.append('/Users/eli/Python/personal_projects/')

import user_config as uc
sender = uc.sender
# this is the app password associate with sender gmail account, only app password available for gmail app after May 2022
password = uc.password
recipients_eli =uc.recipients_eli
general_recipients = uc.general_recipients 



# In[48]:


# sending to owner include txt file to keep track of script info
start_time = time.time()
send_email(subject, body, sender, recipients_eli, password, output_pdf, output_xlsx, output_txt)
print("--- %s mintues " % float( '%.5g' % ((time.time() - start_time)/60)) + 'to complete Sending Emails --------')


# In[49]:


# sending to general recipients only show charts & flight records
start_time = time.time()
send_email(subject, body, sender, general_recipients, password, output_pdf, output_xlsx, None)
print("--- %s mintues " % float( '%.5g' % ((time.time() - start_time)/60)) + 'to complete Sending Emails --------')

