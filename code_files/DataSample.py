
class DataSample:
    '''
    Data Sample Class represents a single sample:
    timestamp in seconds
    speed in meters per seconds
    pressure in pascal
    gps_point contains latitude and longitude coordinates
    distance_delta_from_last_sample the distance in meters that the car passed from last sample
    '''
    def __init__(self, timestamp, speed, pressure, gps_point, distance_delta_from_last_sample):
        self.timestamp = timestamp
        self.speed = speed
        self.pressure = pressure
        self.gps_point = gps_point
        self.distance_delta_from_last_sample = distance_delta_from_last_sample
