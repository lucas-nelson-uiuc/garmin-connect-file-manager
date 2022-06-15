import os
import pandas as pd

def gather_activities_data(export_dir, backup_dir):
    csv_list = [
        pd.read_csv(f'{export_dir}/{export}/{file}')
        for export in os.listdir(export_dir)
        for file in os.listdir(f'{export_dir}/{export}')
        if file.startswith('activities') and file.endswith('.csv')
    ]
    csv_data = pd.concat(csv_list)\
        .drop_duplicates(subset='Activity ID', keep='last')\
        .dropna(axis=1, how='all')\
        .sort_values('Start Time')\
        .reset_index(drop=True)
    csv_data.drop(columns=(csv_data.sum(axis=0) == 0).index[csv_data.sum(axis=0) == 0], inplace=True)

    csv_data.to_pickle(f'{backup_dir}/activities_reference.pkl')
    assert os.path.isfile(f'{backup_dir}/activities_reference.pkl'), FileNotFoundError
    return csv_data.shape[0]