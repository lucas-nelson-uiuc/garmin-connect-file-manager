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
    '''
    Caller function for DIRhelper functions

    Parameters
    ----------
    *kwargs: tuple(kwarg=val, ... )
        kwarg -> title of table displaying directory information
        val   -> str: path to directory
    
    Example
    -------
    >>> directory_status(export_directory='../export-garmin-connect')

                                 EXPORT_DIRECTORY [../export-garmin-connect]                                  
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Directory                        ┃ Gpx_Files ┃ Gpx_Sizes ┃ Json_Files ┃ Json_Sizes ┃ Pkl_Files ┃ Pkl_Sizes ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ 2022-03-16_garmin_connect_export │ 237       │ 58952248  │ 7          │ 1599888    │ 0         │ 0         │
    │ 2022-03-17_garmin_connect_export │ 1         │ 441798    │ 4          │ 15318      │ 0         │ 0         │
    │ 2022-03-19_garmin_connect_export │ 1         │ 362652    │ 4          │ 13999      │ 0         │ 0         │
    │ 2022-03-22_garmin_connect_export │ 3         │ 1083357   │ 4          │ 24526      │ 0         │ 0         │
    │ 2022-03-24_garmin_connect_export │ 3         │ 1083707   │ 4          │ 24569      │ 0         │ 0         │
    │ 2022-03-28_garmin_connect_export │ 1         │ 506637    │ 4          │ 14010      │ 0         │ 0         │
    │ 2022-03-31_garmin_connect_export │ 1         │ 385970    │ 4          │ 14006      │ 0         │ 0         │
    │ 2022-05-17_garmin_connect_export │ 20        │ 7416137   │ 4          │ 115363     │ 0         │ 0         │
    │ 2022-06-04_garmin_connect_export │ 30        │ 12060046  │ 4          │ 168450     │ 0         │ 0         │
    │ TOTAL                            │ 297       │ 82292552  │ 39         │ 1990129    │ 0         │ 0         │
    └──────────────────────────────────┴───────────┴───────────┴────────────┴────────────┴───────────┴───────────┘
    '''

    for param, dir in kwargs.items():
        print_dir_df(param, dir)
