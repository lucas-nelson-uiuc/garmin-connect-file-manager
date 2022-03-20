import pandas as pd
from datetime import datetime
import gpxpy
import pytz
from haversine import haversine, Unit


def read_gpx_file(file_path):
    gpx_file = open(file_path)
    return gpxpy.parse(gpx_file)

def gpx_to_dataframe(file_path):

    points_skeleton = [
        [point.latitude, point.longitude, point.elevation, point.time]
        for track in read_gpx_file(file_path).tracks
        for segment in track.segments
        for point in segment.points
    ]

    points_df =  pd.DataFrame(
        points_skeleton,
        columns=['latitude', 'longitude', 'elevation', 'time']
    ).fillna({'elevation':0})
    
    return points_df

def convert_date(time_col):
    return pd.to_datetime(time_col.dt.date)

def convert_time(time_col):
    return time_col.dt.time

def get_elevation_diff(elev_col):
    return elev_col.diff(1).fillna(0)

def get_shifted_col(col):
    return col.shift(1)

def calculate_haversine(list_de_lat_lon):
    lat1, lon1, lat2, lon2 = list_de_lat_lon
    return haversine(
        (lat1, lon1), (lat2, lon2),
        unit=Unit.METERS
    )

def get_moving_average_col(col, ma=5):
    return col.rolling(window=ma).mean().fillna(method='bfill')

def calculate_gradient(elev_diff_col, dist_col):
    elev_diff_ma5 = get_moving_average_col(elev_diff_col)
    dist_col_ma5 = get_moving_average_col(dist_col)
    return elev_diff_ma5 / dist_col_ma5

def drop_cols(df, *args):
    return df.drop(columns=list(args))

def time_to_tz_native(t, tz_in, tz_out):
    return tz_in.localize(datetime.combine(datetime.today(), t)).astimezone(tz_out).time()

def convert_timezone(time):
    return time_to_tz_native(
        time,
        pytz.utc,
        pytz.timezone(pytz.all_timezones[pytz.all_timezones.index('America/Chicago')])
    )
