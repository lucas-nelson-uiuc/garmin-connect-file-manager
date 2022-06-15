import os
import sys
from datetime import datetime

from alive_progress import alive_bar
from numpy import array, array_equal

import JSONmanager as jm
import GPXmanager as gm
import CSVmanager as cm
import DIRhelper as dh


def validate_arguments(*args):
    counter = 0
    for dir in args[0]:
        assert os.path.exists(dir), f'{dir} does not exist'
        assert os.path.isdir(dir), f'{dir} is not a directory'
        if '.DS_Store' in os.listdir(dir):
            os.remove(f'{dir}/.DS_Store')
        counter += 1
    assert counter == 2, \
        'Expected two arguments: python3 gcfm.py <backup-directory> <export-directory>'
    return args[0]


def fetch_activities_json(subdir_path):
    json_fp = list(filter(
        lambda f: f.startswith('activities') and f.endswith('.json'),
        os.listdir(subdir_path)
        ))[0]
    return f'{subdir_path}/{json_fp}'


if __name__ == '__main__':
    
    args = validate_arguments(sys.argv[1:])
    backup_dir = args['backup' in args[1]]
    export_dir = args[backup_dir == args[0]]

    print()
    dh.directory_status(export_directory=export_dir)
    print()
    
    # with alive_bar(
    #     total=len(os.listdir(export_dir)),
    #     dual_line=True,
    #     title='Converting JSON files ',
    #     spinner='waves3',
    #     bar='filling',
    #     monitor='[{percent:.2f}%] {count}/{total}',
    #     stats='({eta})',
    #     force_tty=True,
    #     ctrl_c=True
    # ) as bar:
    #     for subdir in sorted(os.listdir(export_dir)):
    #         try:
    #             raw_json_fp = fetch_activities_json(f'{export_dir}/{subdir}')
    #             jm.raw_json_to_reuben_json(raw_json_fp, backup_dir)
    #             bar()
    #         except FileNotFoundError:
    #             print('<Error: file not found>')

    with alive_bar(
        total=5,
        dual_line=True,
        title='Collecting user data  ',
        spinner='waves3',
        bar='filling',
        monitor='[{percent:.2f}%] {count}/{total}',
        stats='({eta})',
        force_tty=True,
        ctrl_c=True
    ) as bar:

        bar.text = '  -> Gathering user statistics'
        total_activities = jm.gather_user_stats(export_dir, backup_dir)
        bar()

        bar.text = '  -> Gathering activity IDs'
        activityIDs = jm.gather_activity_ids(export_dir)
        bar()

        bar.text = '  -> Gathering JSON activities'
        activity_df_ids = jm.gather_exhaused_activities(export_dir, backup_dir)
        bar()

        bar.text = '  -> Gathering CSV activities'
        csv_num_rows = cm.gather_activities_data(export_dir, backup_dir)
        bar()

        # ensuring consistency in number of activities
        bar.text = '  -> Checking consistency across database'
        assert total_activities == len(activityIDs) == activity_df_ids.shape[0] == csv_num_rows,\
            'Inconsistent number of activities'
        # ensuring uniqueness in activityIDs
        bar.text = '  -> Checking uniqueness across database'
        assert array_equal(array(list(map(lambda x: int(x), sorted(activityIDs)))), activity_df_ids),\
            'Non-unique IDs found in database'
        print('  -> Tests successful!')
        bar()


    for sub_dir in sorted(os.listdir(export_dir)):
        gpx_files = map(
                lambda g: f'{export_dir}/{sub_dir}/{g}',
                filter(
                    lambda f: f.endswith('.gpx'),
                    os.listdir(f'{export_dir}/{sub_dir}')
                    )
                )
        with alive_bar(
            total=len(os.listdir(f'{export_dir}/{sub_dir}')),
            dual_line=True,
            title=f"Exporting {datetime.strptime(sub_dir[:sub_dir.find('_')], '%Y-%m-%d').strftime('%b %d, %Y')}",
            spinner='waves2',
            bar='filling',
            monitor='[{percent:.2%}] {count}/{total}',
            stats='(ETA: {eta})',
            force_tty=True,
            ctrl_c=True) as bar:
            for gpx_file in gpx_files:
                try:
                    gm.raw_gpx_to_reuben_gpx(gpx_file)
                    gm.write_to_id_dir(gpx_file, backup_dir, extension='pkl')
                    bar()
                except:
                    bar.text = "\t< No GPX Points > {}".format(
                        gpx_file[gpx_file.rfind('_') + 1 : gpx_file.find('.gpx')]
                    )
                    continue

    print()
    dh.directory_status(backup_directory=backup_dir)
    print()
