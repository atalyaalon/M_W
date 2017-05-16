import pandas as pd
from code_files.GPSPoint import GPSPoint
from code_files.DataSample import DataSample

# represents a Driving Session
# contains the data samples and the vin number of the vehicle for each driving session
class DrivingSession:
    # static variable - DrivingSession counter
    counter = 0

    def __init__(self, file_name):

        # increase count of DrivingSessions
        DrivingSession.counter += 1

        # CSV existing column names
        self.TIMESTAMP = 'Timestamp [ms]'
        self.LOCATION = 'External Location'
        self.SPEED = 'Speed [Km/h]'
        self.PRESSURE = 'Pressure [Pa]'
        self.VIN = 'VIN'

        # CSV new column names
        self.LATITUDE = 'Latitude'
        self.LONGITUDE = 'Longitude'

        # samples grouping size
        self.GROUPING_SIZE = 100

        # DrivingSessions Vars
        self.file_name = file_name
        self.df = pd.read_csv(self.file_name, low_memory=False)
        self.vin_num = self.get_first_non_empty_value(self.VIN)
        self.samples = []
        self.get_samples_from_csv()

    def get_samples_from_csv(self):
        # split location to latitude and longitude, update their data-type to float
        self.df[self.LATITUDE], self.df[self.LONGITUDE] = self.df[self.LOCATION].str.split(' ', 1).str
        self.df[self.LATITUDE] = self.df[self.LATITUDE].astype(float)
        self.df[self.LONGITUDE] = self.df[self.LONGITUDE].astype(float)
        # take relevant columns only
        self.df = self.df[[self.TIMESTAMP, self.SPEED, self.PRESSURE, self.LATITUDE, self.LONGITUDE]]
        # use linear intepolation on data (cells with NaN)
        self.df.interpolate(inplace=True)
        # remove rows with Nan cells (removes first rows only, that the interpolation didn't work for them
        self.df.dropna(inplace=True)

        # creates DataSample for each row in the DataFrame df and adds it to the current DrivingSession
        prev_speed_in_meters_per_seconds = 0
        prev_timestamp_in_seconds = 0
        for i, row in self.df.iterrows():
            curr_timestamp_in_seconds = row[self.TIMESTAMP] / float(1000)
            curr_speed_in_meters_per_seconds = row[self.SPEED] / 3.6
            curr_pressure = row[self.PRESSURE]
            curr_latitude = row[self.LATITUDE]
            curr_longitude = row[self.LONGITUDE]
            distance_delta_from_last_sample = prev_speed_in_meters_per_seconds * (curr_timestamp_in_seconds - prev_timestamp_in_seconds)

            data_sample = DataSample(curr_timestamp_in_seconds, curr_speed_in_meters_per_seconds, curr_pressure,
                                     GPSPoint(latitude=curr_latitude, longitude=curr_longitude), distance_delta_from_last_sample)
            self.add_single_sample(data_sample)

            # update prev vars
            prev_speed_in_meters_per_seconds = curr_speed_in_meters_per_seconds
            prev_timestamp_in_seconds = curr_timestamp_in_seconds

    def get_first_non_empty_value(self, column_name):
        column = self.df[column_name].dropna()
        if not column.empty:
            return column.iloc[0]
        else:
            return None

    def add_single_sample(self, data_sample):
        self.samples.append(data_sample)
