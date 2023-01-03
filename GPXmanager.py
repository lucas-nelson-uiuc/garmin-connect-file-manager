import os
import json
import warnings; warnings.filterwarnings('ignore')

import GPXcleaner as gc
import FITmanager as fm


def raw_gpx_to_reuben_gpx(gpx_path):
    '''
    Converts activity.gpx -> pandas.DataFrame  -> activity.pkl

    Parameters
    ----------
    gpx_path: str
        path to .gpx file
    
    Returns
    -------
    pandas.DataFrame
        containing meaningful data from provided .gpx file
    '''
    
    raw_df = gc.gpx_to_dataframe(gpx_path)
    
    # create copy of dataframe for security
    points_df = raw_df.copy()

    # add identifier column
    points_df['activity_id'] = gpx_path[gpx_path.rfind('activity_') + 9:gpx_path.rfind('.gpx')]

    # convert date and time to respective datetime.objects
    points_df['date'] = gc.convert_date(points_df['time'])
    points_df['time'] = gc.convert_time(points_df['time'])

    # change in elevation between measurements
    points_df['elevation_diff'] = gc.get_elevation_diff(points_df['elevation'])
    
    # latitude/longitude of n=1 future observation
    points_df['proj_latitude'] = gc.get_shifted_col(points_df['latitude']).fillna(points_df['latitude'].iloc[0])
    points_df['proj_longitude'] = gc.get_shifted_col(points_df['longitude']).fillna(points_df['longitude'].iloc[0])
    
    # distance between observed point and n=1 future point
    points_df['distance'] = points_df[['latitude', 'longitude', 'proj_latitude', 'proj_longitude']
        ].apply(gc.calculate_haversine, axis=1)
    
    # convert to local time
    points_df['local_time'] = points_df['time'].apply(gc.convert_timezone)
    
    # get time differences to calculate speeds
    points_df['time_elapsed'] = points_df['local_time'].apply(
        lambda x: (x.hour * 60**2) + (x.minute * 60**1) + (x.second * 60**0)
    )
    points_df['time_between_measure'] = points_df['time_elapsed'].diff(1).fillna(0).astype(int)
    points_df['speed_kmh'] = points_df['speed_kmh'] = points_df[['distance', 'time_between_measure']].apply(lambda x: (x[0]/x[1]) * 3.6, axis=1).fillna(0)

    # get power (watts) data
    points_df['power'] = fm.return_power_data(gpx_path, n=points_df.shape[0])

    # smooth (using moving average) speed and gradient
    points_df['speed_kmh_ma5'] = gc.get_moving_average_col(points_df['speed_kmh'])
    points_df['gradient'] = gc.calculate_gradient(points_df['elevation_diff'], points_df['distance'])
    points_df['gradient_ma5'] = gc.get_moving_average_col(points_df['gradient'])
    points_df['heart_rate_ma5'] = gc.get_moving_average_col(points_df['heart_rate'])

    # return the bad boy
    return gc.drop_cols(points_df, 'time_between_measure', 'proj_latitude', 'proj_longitude')


def write_to_id_dir(gpx_path, backup_dir, extension='pkl'):
    '''
    Navigating function for .gpx file to .pkl frame

    Parameters
    ----------
    gpx_path: str
        path to .gpx file
    backup_dir: str
        path to backup directory
    extension: str (default='pkl')
        file extension for writing activity frame
    
    Returns
    -------
    None
    '''
    
    gpx_df = raw_gpx_to_reuben_gpx(gpx_path)
    gpx_file_id = gpx_path[gpx_path.rfind('_') + 1 : gpx_path.find('.gpx')]

    activity_dirs = filter(lambda x: not (x.startswith('.') or x.endswith('.csv') or x.endswith('.pkl') or x.endswith('.json')), os.listdir(backup_dir))
    for activity in activity_dirs:
        if not activity in ['activities_reference.pkl', '.DS_Store', 'user_overview.json', 'activities_exhausted.pkl', 'activiites']:
            activity_ids = json.load(open(f'{backup_dir}/{activity}/{activity.lower()}_ids.json'))
            if int(gpx_file_id) in activity_ids:
                gpx_file_dir = activity

    gpx_file_dir = 'Cycling' if activity in ['Cycling', 'Road_Biking', 'Virtual_Ride'] else activity

    gpx_file_path = f'{backup_dir}/{gpx_file_dir}/{gpx_file_id}.{extension}'
    
    if os.path.isfile(gpx_file_path):
        return
    
    if not os.path.isfile(gpx_file_path):
        if extension == 'pkl':
            gpx_df.to_pickle(gpx_file_path)
        if extension == 'csv':
            gpx_df.to_csv(gpx_file_path)
        if extension == 'sql':
            gpx_df.to_sql(gpx_file_path)
    else:
        print('uh-oh')
