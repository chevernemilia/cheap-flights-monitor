
import time
from time import sleep, strftime
from random import randint

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# import Alert 
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains

# customized module import
from cft_modules.clean_organize import * 
from cft_modules.data_format import *


def load_more(driver):
    main_window = driver.window_handles[0]
#   if multiple windows popup, always closed up the extra windows
    for i in range(1,len(driver.window_handles)):
        popup_window = driver.window_handles[i]

        driver.switch_to.window(popup_window)
        time.sleep(1)
        driver.close()

    #     finally always make driver pointing to main/parent windowx actively
        driver.switch_to.window(main_window) #or driver.switch_to_default_content()

#     print('OUTSIDE IF: current driver window handle:', driver.window_handles) 

    try:
        # Find the popup element using its XPath with multiple attribute string pattern contents of the same element tag
        popup_elm_text = '//div[contains(@class, "dDYU-close")][(@role="button")]'
        popup_elm = driver.find_element("xpath",popup_elm_text)
        attr_of_popup = popup_elm.get_attribute("class")
#         print("attr_of_popup", attr_of_popup)
        popup_elm.click()
    except:
        pass
        
#     kayak price, button  & results xpath elements contents has been updated after 1/1/2023
#     in Q4 2022 the price, button & result element are such:
#      cheap_results = '//a[@data-code = "price"]'
#     more_results = '//a[@class = "moreButton"]'
#     xp_results_table = '//*[@class ="resultWrapper"]'

#   after 2023, Q1 2023, the button & result element are such:
#     cheap_results = '//*[contains(@class, "price-text")]'
#     more_results = '//*[text()="Show more results"]'

#     find element by text
#     this is to click more times to get more result
#     more_results = '//*[text()="Show more results"]'
    more_results = '//*[contains(text(), "Show more results")]'

    button_elm = driver.find_element("xpath", more_results)
#     button_elm = driver.find_element("xpath",more_results)
    
    attr_of_button = button_elm.get_attribute("class")
    button_elm.click()

    # Printing these notes during the program helps me quickly check what it is doing
    print('sleeping.....')
    sleep(randint(10,15))
#         sleep(randint(10,20))
#         sleep(randint(6,12))






def get_cheap_flights(city_from, city_to, flight_date, nbr_dt_range_search, nbr_click_this_session):
    # combine everything together

    # start counting how long it takes to run the script
    start_time = time.time()

    # display all parameter values for current search
    print('city_from: ' , city_from)
    print('city_to: ' , city_to)
    print('flight_date: ' , flight_date)
    print('nbr_dt_range_search: ' , nbr_dt_range_search)
    print('nbr_click_this_session: ' , nbr_click_this_session)

    # a new window would pop up
    chromedriver_path = '/Users/eli/eli_venv/lib/python3.7/site-packages/chromedriver'
#     driver = webdriver.Chrome(executable_path=chromedriver_path) # This will open the Chrome window instance
    driver = webdriver.Chrome(chromedriver_path) 

    driver.maximize_window()
    driver.implicitly_wait(10) # gives an implicit wait for 20 seconds

    print('Search Link: \n')
    if (nbr_dt_range_search == 1):
    ###########################################################################################
    #     one-way with  from and to destination with an (exact date)
        kayak = 'https://www.kayak.com/flights/' + str(city_from) +'-' +str(city_to) +'/' + str(flight_date) +'?sort=bestflight_a&fs=stops=-2'
        print(kayak)
    ###########################################################################################
    else:
    ###########################################################################################
        # one-way with  from and to destination with a from date with <= 1 stop (date range)
        kayak = 'https://www.kayak.com/flights/' + str(city_from) +'-' +str(city_to) +'/' + str(flight_date) +'-' + 'flexible-' + str(nbr_dt_range_search) + 'day?sort=bestflight_a'
        print(kayak)
    ###########################################################################################

    # make sure there's a long interval between each get API so to prevent reCaptcha check
    driver.get(kayak)
#     print('Driver: ', driver)
    # sleep(3)
    sleep(randint(10,15))

    all_flight_list = []

    # click for price first time
    # click for price first time
    # cheap_results = '//a[@data-code = "price"]' --this one deprecated since the xpath of price in kayak url become dynamic 
    # try navigate to the price, inspect, find the code, copy -> copy xpath ( this copy will be xpath contains dynamic web element @id codes)
    # but going to the same price inspect allow to see the static text, and will be more reliable here    
    cheap_results = '//*[contains(@class, "price-text")]'
    driver.find_element("xpath", cheap_results).click()
    

#   nbr of additional times to click for result, each click is 15 rows
 #   these couple lines allow more click within same datetime location search, TBC due to technical issues
    for i in range(nbr_click_this_session):
        load_more(driver)
#         print("loading:", i)


    #     find element by specific attribute values
    result_elm_txt_1 = '//*[@class ="resultWrapper"]'
    # find element by the unique attribute name: still challenging to locate element by a custom attribute key: data-resultid with dynamic token value in each
    # let's hope the class of it is consistent...
    # driver.find_elements(By.CLASS_NAME, 'nrc6')  # this allow finding ALL elements with the same class atrribute name

    # since both result_elm_txt_1 & result_elm_txt_2 existed by the time of current development in Q1 2023,
    # will see if result_elm_txt_2 existed if not use the old way result_elm_txt_1
    try: 
        flight_containers = driver.find_elements(By.CLASS_NAME, 'nrc6')
        if (len(flight_containers) == 0):
            print("Data crawl by 'nrc6' have NO ERROR but return empty list. Use 'ResultWrapper' attribute.")
            flight_containers = driver.find_elements("xpath",result_elm_txt_1)
    except:
        print("Data crawl by 'nrc6' throw ERROR. Use 'ResultWrapper' attribute.")
        flight_containers = driver.find_elements("xpath",result_elm_txt_1)
    
#     print("flight_containers: ", flight_containers)

    # print(flight_containers)
    flight_list = [flight.text for flight in flight_containers]
    flight_list
    print('INSIDE get_cheap_flights FUNCTION: Nbr of flights in this search ssessions:\n')
    print(len(flight_list))

# #     want to closed all window/browser after each set of searches
#     handles = driver.window_handles
#     # Iterate over the list of handles and close each window, 
#     for handle in handles:
#         driver.switch_to.window(handle)
#         driver.close()

    if (len(flight_list) != 0):
        ############## convert all events in flight_list into df based on either exact date or date range########################################################
        flight_df_price = get_exact_dt_flight_price_info_df(flight_list)
        
        if (nbr_dt_range_search ==1):
            flight_df_logistics =  get_exact_dt_flight_logistics_info_df(flight_list, flight_date)
        else:
            flight_df_logistics =  get_multi_dt_flight_logistics_info_df(flight_list)

        # index only use for merging two df
        flight_df_joint = pd.merge(flight_df_logistics, flight_df_price, left_index = True, right_index = True)
        flight_df_joint.drop(columns = 'index', inplace = True)
        # order the columns in my preference
        flight_df_joint = flight_df_joint.reindex(columns = ['date','time', 'airline', 'nbr_stop', 'intermediate_stop', 'duration', 'from',
                'to', 'checked_bag','carry_on_bag', 'price', 'price2','price3', 'price4', 'lowest_price'])

        flight_df_joint['flight_hr'] = convert_duration_str_to_int(flight_df_joint['duration'])
        flight_df_joint['date'] = flight_df_joint['date'].astype(str)

        flight_df_joint['datetime'] = flight_df_joint['date'] + " - " + flight_df_joint['time']
            
        # this is only applicable for multi days search where the query date format available are diff:
        # for single day search the date used in df would be yyyy-mm-dd whereas in multi days search the date query are (m)m/(d)d
        ############################ format the string date with prefix "0" if mo/dt are single digit, easier to sort#################################
        if (nbr_dt_range_search != 1):
            fmt_date_list = []
            for idx, date in enumerate(flight_df_joint['date']):
                mo_dt_list = date.split("/")
                mo_dt_list[0] = '0' + mo_dt_list[0] if len(mo_dt_list[0]) == 1 else mo_dt_list[0]
                mo_dt_list[1] = '0' + mo_dt_list[1] if len(mo_dt_list[1]) == 1 else mo_dt_list[1]
                fmt_date = mo_dt_list[0] + "/" + mo_dt_list[1]
                fmt_date_list.append(fmt_date)
            flight_df_joint['date'] = fmt_date_list
        ############################ end format the string date with prefix "0" if mo/dt are single digit, easier to sort#################################
        
        flight_df_joint = flight_df_joint.fillna(0)

        flight_df_joint = flight_df_joint[flight_df_joint['flight_hr'] != 0 ]
        # flight_df_joint.drop(flight_df_joint[flight_df_joint['flight_hr'] == 0 ].index, inplace = True)

        flight_df_joint = flight_df_joint.sort_values(by = ['lowest_price', 'flight_hr'])
        flight_df_joint
        print("--- %s mintues " % float( '%.5g' % ((time.time() - start_time)/60)) + 'to complete this seach session. --------')

        return(flight_df_joint)

    else:
        print("No flights were searched for destination: ", city_to)
        print('------------------------------------------------------------------------------------------------\n')
        next

