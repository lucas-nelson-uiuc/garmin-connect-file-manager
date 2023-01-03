import os
import json
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def angleFromCoordinate(cols_list):
    import math
    lat1, long1, lat2, long2 = cols_list
    dLon = (long2 - long1)

    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)

    brng = math.atan2(y, x)

    brng = math.degrees(brng)
    brng = (brng + 360) % 360
    brng = 360 - brng # count degrees clockwise - remove to make counter-clockwise

    return brng

def modify_to_timedelta(wind_time):
    return pd.to_timedelta(pd.to_datetime(wind_time).time().strftime('%H:%M:%S'))

def gather_lowest_idx(df, local_time):
    local_time = pd.to_timedelta(local_time.strftime('%H:%M%:%S'))
    idx = (np.abs(df['time_delta'] - local_time)).argmin()
    return df[['drct', 'sped']].iloc[idx]

