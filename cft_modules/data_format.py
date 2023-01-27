

import re

def convert_duration_str_to_int(duration_str_col):
    duration_hr_list = []
    # for i in flight_df_joint['duration']:
    for i in duration_str_col:
        
#         print(i)
        duration_int = re.findall(r'\d+', i)
    
#     some flight rows just missing the intermediate des with multiple stops, that might affect the data val cleaning into right fields
#         info of the flight might be insufficient, duration_hr were off column so let's skip such row for simplicity
#       so assign duration_hr to 0 when there is no legit int val for hr/min within the alphanumeric string feature based on parsing
        if len(duration_int) !=0:
            duration_hr = int(duration_int[0]) + round(int(duration_int[1])/ 60, 2)
        else: duration_hr = 0 
 
        duration_hr_list.append(duration_hr)   
    return(duration_hr_list)
