import os
import sys

import JSONcleaner as jsc
import DIRhelper as dh


def raw_json_to_reuben_json(activities_json_file_path, backup_dir):

    raw_json = jsc.gather_json_content(activities_json_file_path)
    raw_df = jsc.convert_json_to_df(raw_json)
    raw_cp = raw_df.copy()
    raw_cp[['startDateLocal', 'startTimeLocal']] = jsc.extract_local_datetime(raw_cp['startTimeLocal'])

    # fixing up dictionary value column
    raw_cp['activityType'] = jsc.extract_activity_type(raw_cp['activityType'])

    # columns where NA -> 0.0
    fill_zero_cols = [
        'aerobicTrainingEffect',
        'anaerobicTrainingEffect',
        'activityTrainingLoad',
        'moderateIntensityMinutes',
        'vigorousIntensityMinutes'
        ]
    raw_cp[fill_zero_cols] = jsc.fill_na_vals(raw_cp, fill_zero_cols)

    # columns where NA -> previous_value
    fill_back_cols = ['vO2MaxValue']
    raw_cp[fill_back_cols] = jsc.fill_na_vals(raw_cp, fill_back_cols, fill_method='bfill')

    # reordering for convenience
    reuben_df = raw_cp[['activityId', 'startTimeLocal', 'startDateLocal'].__add__(list(raw_cp.columns[2:-1]))]

    success, failure, total = 0,0,0
    for idx in range(reuben_df.shape[0]):
        
        json_temp = reuben_df.iloc[idx]
        
        # extract meaningful file naming information
        json_file_id = f"{'-'.join(json_temp['startDateLocal'].split(' '))}-{json_temp['activityId']}"
        json_file_dir = json_temp['activityType'].title()

        # construct file path from information above
        json_activity_dir = f'{backup_dir}/{json_file_dir}'
        # json_id_dir = f''
        json_file_path = json_activity_dir + f'/{json_file_id}.json'
        
        # check for uniqueness of file ID
        if not os.path.isdir(json_activity_dir):
            os.mkdir(json_activity_dir)
        
        if not os.path.isfile(json_file_path):
            
            # write to respective file path in format (orient)
            # such that it can be easily accessed in future -
            # similar to pd.DataFrame.to_dict()
            with open(json_file_path, 'w') as f:
                json_temp.to_json(
                    f,
                    orient='split',
                    force_ascii=False
                    )
                
            # check if this shit worked
            if os.path.isfile(json_file_path):
                success += 1; total += 1
                print(
                    '\tSuccess {:<12}: {}'.format(
                        f'[{success}/{total}]',
                        json_file_path
                    )
                )
            else:
                failure += 1; total += 1
                print(
                    '\tFailure {:<12}: {}'.format(
                        f'[{failure}/{total}]',
                        json_file_path
                    )
                )
    
    print()
