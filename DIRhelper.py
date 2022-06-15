import os
import json

from pandas.core.frame import DataFrame

import rich
from rich.table import Table


def get_dir_info(dir):
    
    if (len([d for d in os.listdir(dir) if not os.path.isdir(f'{dir}/{d}')]) == len(os.listdir(dir))):
        return {dir : {'empty' : {
            'gpx_files':0, 'gpx_sizes':0,
            'json_files':0, 'json_sizes':0,
            'pkl_files':0, 'pkl_sizes':0}}}
    
    # keep in case merge both dictionaries
    retr_dict = {dir: {}}
    for subdir in sorted(os.listdir(dir)):
        
        if (subdir == '.DS_Store') or (subdir.endswith('.pkl')) or (subdir.endswith('.json')):
            continue
        
        retr_dict[dir][subdir] = {
            'gpx_files':0, 'gpx_sizes':0,
            'json_files':0, 'json_sizes':0,
            'pkl_files':0, 'pkl_sizes':0}
        filtered_subdir = [
            f
            for f in os.listdir(f'{dir}/{subdir}')
            if f.endswith('.gpx') or f.endswith('.json') or f.endswith('.pkl')]
        
        for file in filtered_subdir:
            file_extension = file[file.rfind('.') + 1 : ]
            retr_dict[dir][subdir][f'{file_extension}_files'] += 1
            retr_dict[dir][subdir][f'{file_extension}_sizes'] += os.path.getsize(f'{dir}/{subdir}/{file}')
    
    return retr_dict


def dir_info_to_dir_df(dir_info):
    '''
    Return dataframe with information of current
    directory's information, such as total activities,
    activity types, and corresponding descriptive statistics

    | Parameters |
    > dir_info
        Returned value from get_dir_info, a dictionary
        containing descriptive statistics of a provided directory
    '''

    dir_idxs = list(dir_info.values())[0].keys()
    dir_vals = list(list(dir_info.values())[0].values())
    dir_df = DataFrame(dir_vals, index=dir_idxs)
    dir_df.loc["TOTAL"] = dir_df.sum()
    return dir_df


def print_dir_df(param, dir):
    '''
    Display directory statistics to terminal

    | Parameters |
    > param
    > dir
    '''

    dir_df = dir_info_to_dir_df(get_dir_info(dir))
    table = Table(
        title=f'{param.upper()} [{dir}]',
        style='bold magenta'
        )
    table.add_column(
        'Directory',
        justify='left',
        style='cyan'
    )
    for col in dir_df.columns:
        table.add_column(
            col.title(),
            justify='left',
            style='cyan'
        )
    for i in range(dir_df.shape[0]):
        d1 = dir_df.index[i]
        table.add_row(d1, *tuple([str(elem) for elem in dir_df.iloc[i, :]]))
    
    rich.print(table)


def directory_status(**kwargs):    
    for param, dir in kwargs.items():
        print_dir_df(param, dir)
