
import pandas as pd
import numpy as np  
import re



# get both the nbr of luggages provided for free & all price available, apply to both exact day and day range search
def get_exact_dt_flight_price_info_df(flight_list):

    flight_info_list = []
    flight_logistic_items_ct_list = []

    flight_df_price = pd.DataFrame()
    # assuming nbr of luggage (carryon, checked can be up to 5 in case)
    keep_row_item_pattern = ['0', '1', '2','3','4','5']

    columns_defined = ['index',  'carry_on_bag', 'checked_bag', 'price', 'price2','price3', 'price4']

    outer_lst_keep = []
    for idx_outer_lst, row in enumerate(flight_list):
        flight_info = row.split('\n')
    #     print(flight_info)
        inner_lst_keep = []
        inner_lst_keep.append(idx_outer_lst)

        for idx_inner_lst, i in enumerate(flight_info):
    #         here only want to get either the baggage nbr or the price amount but should all be single word item within the string
            string_item = i.split(' ')
            nbr_string_item = len(string_item)
            if (i in keep_row_item_pattern or  '$' in i ) and (nbr_string_item ==1):
    #             print(i)

                inner_lst_keep.append(i)

    #     print(inner_lst_keep)
    #     these two positions should implies info. of single digit int for baggage info. not price
        identify_2_bag_info = sum([len(x)==1 for x in inner_lst_keep[1:3]])
    #     print(sum(identify_bag_info))
        if identify_2_bag_info == 1:

            inner_lst_keep.insert(1, '-')
    #         print(inner_lst_keep)
    #     print(len(inner_lst_keep))

        outer_lst_keep.append(inner_lst_keep)
        nbr_logistics_items = len(inner_lst_keep)
        flight_logistic_items_ct_list.append(nbr_logistics_items)

    # print(flight_logistic_items_ct_list)
    flight_max_logistic_items_ct = max(flight_logistic_items_ct_list)
    # print(flight_max_logistic_items_ct)
    # print(columns_defined[:flight_max_logistic_items_ct])
    columns_defined = columns_defined[:flight_max_logistic_items_ct]
    flight_df_price = pd.DataFrame(outer_lst_keep, columns = columns_defined)

    flight_df_price = flight_df_price.fillna(0).replace(np.nan,0)
    flight_df_price
    # drop the row/flight if the basic price cannot be found from the flight_list, no point to include for comparison
    flight_df_price.drop(flight_df_price[flight_df_price['price'] == 0].index, inplace = True)
    flight_df_price['lowest_price'] = [int(''.join(x[1:].split(','))) for x in flight_df_price['price']]
    flight_df_price

    return(flight_df_price)
    

def get_exact_dt_flight_logistics_info_df(flight_list, flight_date):
    
    flight_info_list = []
    flight_df = pd.DataFrame()
    flight_date = flight_date
    flight_date = pd.to_datetime(flight_date)

    columns_defined = ['time', 'airline', 'nbr_stop','intermediate_stop', 'duration', 'from', 'direct_to', 'indirect_to']

    for idx, row in enumerate(flight_list):
        all_flight_info = row.split('\n')

        while not (' pm ' in all_flight_info[0] or ' am ' in  all_flight_info[0]) :
            all_flight_info.pop(0)

        select_flight_info = all_flight_info[:8]      
        flight_info_list.append(select_flight_info)    

        flight_df = pd.DataFrame(flight_info_list, columns = columns_defined)
        flight_df['date'] = flight_date
        flight_df

        # clean up variables values since each event shift left/right arbitrary
        flight_df['to'] = np.where(flight_df['nbr_stop']  == 'nonstop',flight_df['direct_to'], flight_df['indirect_to'])
        flight_df['from'] = np.where(flight_df['nbr_stop']  == 'nonstop', flight_df['duration'], flight_df['from'])
        flight_df['duration'] = np.where(flight_df['nbr_stop']  == 'nonstop',  flight_df['intermediate_stop'], flight_df['duration'])
        flight_df['intermediate_stop'] = np.where(flight_df['nbr_stop']  == 'nonstop', '--', flight_df['intermediate_stop'])
        keep_col = [col for col in flight_df.columns if '_t' not in col]
        flight_df = flight_df[keep_col]

    return(flight_df)



def get_multi_dt_flight_logistics_info_df(flight_list):
    
    flight_info_list = []
    flight_df = pd.DataFrame()
    ####################################start of date range for flight_df############################################
    # this block exectute when multiple days/ a date range is chosen because extra date col need to be extracted
    columns_defined = ['date','wkdate', 'time', 'airline', 'nbr_stop','intermediate_stop', 'duration', 'from', 'direct_to', 'indirect_to']
    for idx, row in enumerate(flight_list):
        all_flight_info = row.split('\n')
        try:
            dt_val_loc_list = [ len(re.findall(r'[0-9]+/+[0-9]+',x)) for x in all_flight_info]
            dt_val_loc = dt_val_loc_list.index(1)
            adj_flight_info = all_flight_info[dt_val_loc:]
            select_flight_info = adj_flight_info[:10] 
            flight_info_list.append(select_flight_info)
        except:
            next

    flight_df = pd.DataFrame(flight_info_list, columns = columns_defined)
    flight_df
    ####################################end of date range for flight_df############################################

        # clean up variables values since each event shift left/right arbitrary
    flight_df['to'] = np.where(flight_df['nbr_stop']  == 'nonstop',flight_df['direct_to'], flight_df['indirect_to'])
    flight_df['from'] = np.where(flight_df['nbr_stop']  == 'nonstop', flight_df['duration'], flight_df['from'])
    flight_df['duration'] = np.where(flight_df['nbr_stop']  == 'nonstop',  flight_df['intermediate_stop'], flight_df['duration'])
    flight_df['intermediate_stop'] = np.where(flight_df['nbr_stop']  == 'nonstop', '--', flight_df['intermediate_stop'])
    keep_col = [col for col in flight_df.columns if '_t' not in col]
    flight_df = flight_df[keep_col]
    return(flight_df)


    