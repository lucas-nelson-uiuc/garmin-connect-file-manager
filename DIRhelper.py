import os

from pandas.core.frame import DataFrame

import rich
from rich.table import Table


def get_dir_info(dir):
    '''
    Gathers file information per subdirectory of passed directory (dir)
    to be passed to dir_info_to_dir_df

    Parameters
    ----------
    dir: str
        path to directory

    Returns
    -------
    dict
        keys: directory (or `empty`)
        vals: dict
            keys: file type/size
            vals: statistic
    '''
    if (len([d for d in os.listdir(dir) if not os.path.isdir(f'{dir}/{d}')]) == len(os.listdir(dir))):
        return {dir : {'empty' : {
            'gpx_files':0, 'gpx_MB':0,
            'json_files':0, 'json_MB':0,
            'pkl_files':0, 'pkl_MB':0}}}
    
    # keep in case merge both dictionaries
    retr_dict = {dir: {}}
    for subdir in sorted(os.listdir(dir)):
        
        if (subdir == '.DS_Store') or (subdir.endswith('.pkl')) or (subdir.endswith('.json') or (subdir.endswith('.csv')) or (subdir.endswith('.gpx'))):
            continue
        
        retr_dict[dir][subdir] = {
            'gpx_files':0, 'gpx_MB':0,
            'json_files':0, 'json_MB':0,
            'pkl_files':0, 'pkl_MB':0}
        filtered_subdir = [
            f
            for f in os.listdir(f'{dir}/{subdir}')
            if f.endswith('.gpx') or f.endswith('.json') or f.endswith('.pkl')]
        
        for file in filtered_subdir:
            file_extension = file[file.rfind('.') + 1 : ]
            retr_dict[dir][subdir][f'{file_extension}_files'] += 1
            retr_dict[dir][subdir][f'{file_extension}_MB'] += round(os.path.getsize(f'{dir}/{subdir}/{file}') / 100000, 2)
    
    return retr_dict


def dir_info_to_dir_df(dir_info):
    '''
    Return dataframe with information of current
    directory's information, such as total activities,
    activity types, and corresponding descriptive statistics

    Parameters
    ----------
    dir_info
        Returned value from get_dir_info, a dictionary
        containing descriptive statistics of a provided directory

    Returns
    -------
    pandas.DataFrame
        rows: directories
        cols: file sizes/types
    '''

    dir_idxs = list(dir_info.values())[0].keys()
    dir_vals = list(list(dir_info.values())[0].values())
    dir_df = DataFrame(dir_vals, index=dir_idxs)
    dir_df.loc["TOTAL"] = dir_df.sum()
    return dir_df


def print_dir_df(param, dir):
    '''
    Gather and display directory statistics to terminal

    Parameters
    ----------
    param: str
        title of directory to be displayed in terminal (e.g. 'backup_directory')
    dir: str
        path to directory

    Returns
    -------
    std.out
        rich.Table printed to terminal
    '''

    dir_df = dir_info_to_dir_df(get_dir_info(dir))
    table = Table(
        title=f'{param.upper()} [{dir}]',
        style='bold magenta'
        )
    table.add_column(
        'Directory',
        justify='right',
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
    '''
    Caller function for DIRhelper functions

    Parameters
    ----------
    *kwargs: tuple(kwarg=val, ... )
        kwarg -> title of table displaying directory information
        val   -> str: path to directory
    
    Example
    -------
    >>> directory_status(backup_dir='../backup-garmin-connect')
                                BACKUP_DIRECTORY [../backup-garmin-connect]                         
    ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
    ┃    Directory ┃ Gpx_Files ┃ Gpx_Mb ┃ Json_Files ┃ Json_Mb ┃ Pkl_Files ┃ Pkl_Mb             ┃
    ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
    │       Cardio │ 0.0       │ 0.0    │ 1.0        │ 0.0     │ 0.0       │ 0.0                │
    │      Cycling │ 0.0       │ 0.0    │ 1.0        │ 0.03    │ 160.0     │ 193.21             │
    │         Golf │ 0.0       │ 0.0    │ 1.0        │ 0.0     │ 3.0       │ 6.98               │
    │  Road_Biking │ 0.0       │ 0.0    │ 1.0        │ 0.01    │ 53.0      │ 84.73999999999998  │
    │       Rowing │ 0.0       │ 0.0    │ 1.0        │ 0.01    │ 54.0      │ 66.05000000000001  │
    │      Running │ 0.0       │ 0.0    │ 1.0        │ 0.01    │ 70.0      │ 50.96              │
    │ Virtual_Ride │ 0.0       │ 0.0    │ 1.0        │ 0.0     │ 14.0      │ 38.43              │
    │      Walking │ 0.0       │ 0.0    │ 1.0        │ 0.0     │ 15.0      │ 25.619999999999994 │
    │        TOTAL │ 0.0       │ 0.0    │ 8.0        │ 0.06    │ 369.0     │ 465.99             │
    └──────────────┴───────────┴────────┴────────────┴─────────┴───────────┴────────────────────┘
    
    >>> directory_status(export_directory='../export-garmin-connect')

                                            EXPORT_DIRECTORY [../export-garmin-connect]                                           
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┓
    ┃                            Directory ┃ Gpx_Files ┃ Gpx_Mb             ┃ Json_Files ┃ Json_Mb            ┃ Pkl_Files ┃ Pkl_Mb ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━┩
    │ 2023-01-02_garmin_connect_export_fit │ 0.0       │ 0.0                │ 14.0       │ 22.849999999999998 │ 0.0       │ 0.0    │
    │ 2023-01-02_garmin_connect_export_gpx │ 413.0     │ 1395.0300000000007 │ 14.0       │ 22.849999999999998 │ 0.0       │ 0.0    │
    │                                TOTAL │ 413.0     │ 1395.0300000000007 │ 28.0       │ 45.699999999999996 │ 0.0       │ 0.0    │
    └──────────────────────────────────────┴───────────┴────────────────────┴────────────┴────────────────────┴───────────┴────────┘
    '''

    for param, dir in kwargs.items():
        print_dir_df(param, dir)
