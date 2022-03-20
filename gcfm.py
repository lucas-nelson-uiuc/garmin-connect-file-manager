import os
import sys

import JSONmanager as jm
import GPXmanager as gm
import DIRhelper as dh


def validate_arguments(*args):
    counter = 0
    for dir in args[0]:
        assert os.path.exists(dir), f'{dir} does not exist'
        assert os.path.isdir(dir), f'{dir} is not a directory'
        if '.DS_Store' in os.listdir(dir):
            os.remove(f'{dir}/.DS_Store')
        counter += 1
    assert counter == 2, 'Not the right amount of arguments'
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

    print('>> CHECKING DIRECTORY INPUTS')
    dh.directory_status(
        backup_directory=backup_dir,
        export_directory=export_dir)
    
    print('>> STARTING BACKUP PROCESS')
    for subdir in sorted(os.listdir(export_dir)):
        print(f'-> {export_dir}/{subdir}')
        raw_json_fp = fetch_activities_json(f'{export_dir}/{subdir}')
        jm.raw_json_to_reuben_json(raw_json_fp, backup_dir)

    print('>> CONVERTING GPX FILES')
    for subdir in sorted(os.listdir(export_dir)):
        print(f'-> {export_dir}/{subdir}')
        gpx_files = map(
            lambda g: f'{export_dir}/{subdir}/{g}',
            filter(
                lambda f: f.endswith('.gpx'),
                os.listdir(f'{export_dir}/{subdir}')
                )
            )
        
        s,f,t = 0,0,0
        for gpx_file in gpx_files:
        
            try:
                gm.raw_gpx_to_reuben_gpx(gpx_file)
            except AttributeError:
                assert len(gm.gc.read_gpx_file(gpx_file).tracks[0].segments[0].points) == 0, \
                    'Something else...'
                f += 1; t += 1
                print('\tNoPoints {}: {}\n'.format(
                    f'[{f}/{t}]',
                    gpx_file))
                continue
        
            s += 1; t += 1
            gm.write_to_id_dir(gpx_file, backup_dir, extension='pkl', success=s, total=t)


    
    print('>> CHECKING UPDATED DIRECTORY STATUS')
    dh.directory_status(
        backup_directory=backup_dir,
        export_directory=export_dir)
    
    print('>> BACKUP PROCESS COMPLETE')
