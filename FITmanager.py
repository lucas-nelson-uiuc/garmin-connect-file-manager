import pandas as pd
import numpy as np
import fitparse



def return_power_data(gpx_path, n):
    fit_path = gpx_path.replace('gpx', 'fit')
    fitfile = fitparse.FitFile(fit_path)
    
    data_dict = {}
    for record in fitfile.get_messages('record'):
        for data in record:
            if data.name not in data_dict:
                data_dict[data.name] = []
            if (data.name in ['distance', 'speed']) and (data.value == None):
                continue
            data_dict[data.name].append(data.value)
    
    if 'power' in data_dict.keys():
        return pd.DataFrame(data_dict)['power']

    return [np.nan] * n
