import os
import rich
from rich.table import Table
from pandas.core.frame import DataFrame


def get_dir_info(dir):
    
    if len(os.listdir(dir)) == 0:
        return {dir : {'empty' : {
            'gpx_files':0, 'gpx_sizes':0,
            'json_files':0, 'json_sizes':0,
            'pkl_files':0, 'pkl_sixes':0}}}
    
    # keep in case merge both dictionaries
    retr_dict = {dir: {}}
    for subdir in sorted(os.listdir(dir)):
        
        if subdir == '.DS_Store':
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
    dir_idxs = list(dir_info.values())[0].keys()
    dir_vals = list(list(dir_info.values())[0].values())
    dir_df = DataFrame(dir_vals, index=dir_idxs)
    dir_df.loc["Total"] = dir_df.sum()
    return dir_df

def print_dir_df(param, dir):
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
        d2,d3,d4,d5,d6,d7 = tuple([str(elem) for elem in dir_df.iloc[i, :]])
        table.add_row(d1,d2,d3,d4,d5,d6,d7)
    
    rich.print(table)

def directory_status(**kwargs):
    
    for param, dir in kwargs.items():
        print_dir_df(param, dir)
