import os
import json
from functools import reduce

from pandas import concat
from pandas.core.frame import DataFrame


def generate_activity_directories(activity_types, activity_ids, backup_dir):
    '''
    Write activity IDs to respective activity type's .json reference file

    Parameters
    ----------
    activity_types: array_like
        array of all activity types per row of activities_df
    activity_ids: array_like
        array of all activity IDs per row of activities_df
    backup_dir: str
        path to backup directory
    
    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        when json file is not written to respective activity directory
    '''
    backup_id_dict = {type.title():[] for type in activity_types}
    
    # populate dictionary like {activity_type:[activity_ids]} for all
    # unique activity_types in activities_df
    for type, id in zip(activity_types, activity_ids):
        if not os.path.isdir(f'{backup_dir}/{type.title()}'):
            os.mkdir(f'{backup_dir}/{type.title()}')
        backup_id_dict[type.title()].append(id)
    
    # "dump" each activity_types information into its respective directory
    # as a .json file
    for activity_key in backup_id_dict:
        with open(f'{backup_dir}/{activity_key}/{activity_key.lower()}_ids.json', 'w', encoding='utf-8') as f:
            json.dump(backup_id_dict[activity_key], f, ensure_ascii=False, indent=4)
        assert os.path.isfile(f'{backup_dir}/{activity_key}/{activity_key.lower()}_ids.json'),\
            f'< FileNotFoundError: {activity_key} >'


def gather_user_stats(export_dir, backup_dir):
    '''
    Obtain user aggregate statistics, such as total activities performed,
    distance covered, time elapsed, calories burned, and elevation gained
    
    Parameters
    ----------
    export_dir: str
        path to export directory
    backup_dir: str
        path to backup directory

    Returns
    -------
    int
        number of activities performed
    
    Raises
    ------
    FileNotFoundError
        when json file is not written to backup directory
    '''
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
    '''
    Gather all unique activity IDs per subdirectory of export_dir

    Parameters
    ----------
    export_dir: str
        path to export directory
    
    Returns
    -------
    list
        collection of all unique activity IDs
    '''
    ids_list = [
        json.load(open(f'{export_dir}/{export}/downloaded_ids.json'))['ids']
        for export in os.listdir(export_dir)
    ]
    return list(set(reduce(lambda x,y: x+y,ids_list)))


def gather_exhaused_activities(export_dir, backup_dir):
    '''
    Gathers all json data from export subdirectories

    Parameters
    ----------
    export_dir: str
        path to export directory
    backup_dir: str
        path to backup directory
    
    Returns
    -------
    array
        collection of activity IDs
    
    Raises
    ------
    FileNotFoundError
        when .pkl file is not written to backup directory
    '''
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
