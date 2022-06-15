import os
import json
from functools import reduce

from pandas import concat
from pandas.core.frame import DataFrame

import JSONcleaner as jsc


# def raw_json_to_reuben_json(activities_json_file_path, backup_dir):

#     raw_json = jsc.gather_json_content(activities_json_file_path)
#     raw_df = jsc.convert_json_to_df(raw_json)
#     raw_cp = raw_df.copy()
#     raw_cp[['startDateLocal', 'startTimeLocal']] = jsc.extract_local_datetime(raw_cp['startTimeLocal'])

#     # fixing up dictionary value column
#     raw_cp['activityType'] = jsc.extract_activity_type(raw_cp['activityType'])

#     # columns where NA -> 0.0
#     fill_zero_cols = [
#         'aerobicTrainingEffect',
#         'anaerobicTrainingEffect',
#         'activityTrainingLoad',
#         'moderateIntensityMinutes',
#         'vigorousIntensityMinutes'
#         ]
#     raw_cp[fill_zero_cols] = jsc.fill_na_vals(raw_cp, fill_zero_cols)

#     # columns where NA -> previous_value
#     fill_back_cols = ['vO2MaxValue']
#     raw_cp[fill_back_cols] = jsc.fill_na_vals(raw_cp, fill_back_cols, fill_method='bfill')

#     # reordering for convenience
#     reuben_df = raw_cp[['activityId', 'startTimeLocal', 'startDateLocal'].__add__(list(raw_cp.columns[2:-1]))]

#     success, failure, total = 0,0,0
#     for idx in range(reuben_df.shape[0]):
        
#         json_temp = reuben_df.iloc[idx]
        
#         # extract meaningful file naming information
#         json_file_id = f"{'-'.join(json_temp['startDateLocal'].split(' '))}-{json_temp['activityId']}"
#         json_file_dir = json_temp['activityType'].title()

#         # construct file path from information above
#         json_activity_dir = f'{backup_dir}/{json_file_dir}'
#         json_file_path = json_activity_dir + f'/{json_file_id}.json'
        
#         # check for uniqueness of file ID
#         if not os.path.isdir(json_activity_dir):
#             os.mkdir(json_activity_dir)
        
#         if not os.path.isfile(json_file_path):
            
#             # write to respective file path in format (orient)
#             # such that it can be easily accessed in future -
#             # similar to pd.DataFrame.to_dict()
#             with open(json_file_path, 'w') as f:
#                 json_temp.to_json(
#                     f,
#                     orient='split',
#                     force_ascii=False
#                     )
                
#             # check if this shit worked
#             assert os.path.isfile(json_file_path), FileNotFoundError


def generate_activity_directories(activity_types, activity_ids, backup_dir):
    backup_id_dict = {}
    
    for type, id in zip(activity_types, activity_ids):
        if not os.path.isdir(f'{backup_dir}/{type.title()}'):
            os.mkdir(f'{backup_dir}/{type.title()}')
            backup_id_dict[type.title()] = []
        backup_id_dict[type.title()].append(id)
    
    for activity_key in backup_id_dict:
        with open(f'{backup_dir}/{activity_key}/{activity_key.lower()}_ids.json', 'w', encoding='utf-8') as f:
            json.dump(backup_id_dict[activity_key], f, ensure_ascii=False, indent=4)


def gather_user_stats(export_dir, backup_dir):
    userstats_list = [
        f'{export_dir}/{export}/userstats.json'
        for export in sorted(os.listdir(export_dir))
    ]
    json_info = json.load(open(userstats_list[-1]))

    user_overview_dict = {
        key : json_info['userMetrics'][0].get(key)
        for key in [
            'total'+k
            for k in ['Activities', 'Distance', 'Duration', 'Calories', 'ElevationGain']
        ]
    }

    with open(f'{backup_dir}/user_overview.json', 'w', encoding='utf-8') as f:
        json.dump(user_overview_dict, f, ensure_ascii=False, indent=4)
    
    assert os.path.isfile(f'{backup_dir}/user_overview.json'), FileNotFoundError
    return user_overview_dict['totalActivities']


def gather_activity_ids(export_dir):
    ids_list = [
        json.load(open(f'{export_dir}/{export}/downloaded_ids.json'))['ids']
        for export in os.listdir(export_dir)
    ]
    return list(set(reduce(lambda x,y: x+y,ids_list)))


def gather_exhaused_activities(export_dir, backup_dir):
    data_list = []
    act_json = [
        json.load(open(f'{export_dir}/{export}/{file}'))
        for export in os.listdir(export_dir)
        for file in os.listdir(f'{export_dir}/{export}')
        if file.startswith('activities-') and file.endswith('.json')
    ]

    for container in act_json:
        if isinstance(container, list):
            for activity in container:
                data_list.append(DataFrame.from_dict(activity, orient='index').T)
        else:
            data_list.append(DataFrame.from_dict(container, orient='index').T)

    activities_df = concat(data_list)\
        .drop_duplicates(subset='activityId', keep='last')\
        .dropna(axis=1, how='all')\
        .sort_values('startTimeLocal')\
        .reset_index(drop=True)
    activities_df.drop(columns=(activities_df.sum(axis=0) == 0).index[activities_df.sum(axis=0) == 0], inplace=True)
    activities_df['activityType'] = activities_df['activityType'].apply(lambda x: x['typeKey'].title()).str.replace('Indoor_', '')

    generate_activity_directories(
        activities_df['activityType'],
        activities_df['activityId'],
        backup_dir
    )

    activities_df.to_pickle(f'{backup_dir}/activities_exhausted.pkl')
    assert os.path.isfile(f'{backup_dir}/activities_exhausted.pkl'), FileNotFoundError
    return activities_df['activityId']
