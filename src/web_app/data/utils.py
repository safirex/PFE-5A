import numpy as np
import math
import pandas as pd

def get_working_hours_stop(timestamps : list, limit_day_iter = 3):
    '''
    timestamp : sorted list of timestamps
    limit_day_iter : number of days to iterate through to determinate the work hours pattern
    '''
    # create a dict with an entree for each hour of the day
    hours = {hour:0 for hour in range(24)}
    
    date_debut = pd.Timestamp(timestamps[0],unit='s')
    for line in timestamps:
        timestamp = pd.Timestamp(line,unit='s')
        hour_conv = timestamp.hour
        print(timestamp)
        hours[hour_conv] = hours[hour_conv]+1
        if( (timestamp - date_debut).days > limit_day_iter ):
            break
        
    return list( filter( lambda x: hours[x]>0, hours.keys() ) ) # get hours with at least one stop