import json
import pandas as pd


def gather_json_content(json_fp):
    return json.load(open(json_fp, 'r'))

def convert_json_to_df(loaded_json):
    if not type(loaded_json) == list:
        loaded_json = [loaded_json]
    return pd.DataFrame(loaded_json)[['activityId',
        'startTimeLocal',
        'activityType',
        'calories',
        'averageHR',
        'maxHR',
        'aerobicTrainingEffect',
        'anaerobicTrainingEffect',
        'vO2MaxValue',
        'locationName',
        'activityTrainingLoad',
        'aerobicTrainingEffectMessage',
        'anaerobicTrainingEffectMessage',
        'moderateIntensityMinutes',
        'vigorousIntensityMinutes'
        ]]

def extract_local_datetime(datetime_col):
    return datetime_col.str.extract('(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})')

def extract_activity_type(activityType_col):
    return activityType_col.apply(lambda x: x['typeKey'].replace('indoor_', ''))

def fill_na_vals(df, na_cols, na_vals=0, fill_method=None):
    return df[na_cols].fillna(na_vals) \
        if fill_method == None \
        else df[na_cols].fillna(method=fill_method)
