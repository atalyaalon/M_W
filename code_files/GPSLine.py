from math import radians, cos, sin, asin, sqrt, atan, degrees
from code_files.GPSPoint import GPSPoint

# represents a GPS Line
class GPSLine:

    def __init__(self, point_a, point_b):

        self.R = 6372000 # earth radius in meters

        if point_b.latitude > point_a.latitude:
            self.lat1, self.lon1 = point_a.latitude, point_a.longitude
            self.lat2, self.lon2 = point_b.latitude, point_b.longitude
        else:
            self.lat1, self.lon1 = point_b.latitude, point_b.longitude
            self.lat2, self.lon2 = point_a.latitude, point_a.longitude

        self.MAX_ERROR_DISTANCE = 70
        self.MAX_ANGLE_ERROR_DEGREES = 10

        self.x, self.y, self.distance_between_points = self.calculate_line_cartesian(self.lat2, self.lon2)

        try:
            self.line_slope = (float(self.y))/(float(self.x))
        except ZeroDivisionError:
            # line is vertical
            self.line_slope = None

    # check if this GPLLine slopes have the same sign to another GPSLine (avoids using wrong points in intersections)
    def lines_slope_signs_similar(self, other_line):
        other_slope = other_line.line_slope
        line_slope = self.line_slope
        return (line_slope and other_slope and (line_slope * other_slope) > 0) or (not line_slope) or (not other_slope)

    # check if the angle between the lines is smaller than the threshold self.MAX_ANGLE_ERROR_DEGREES
    def angle_between_lines_is_appropriate(self, other_line):
        other_slope = other_line.line_slope
        line_slope = self.line_slope
        return (line_slope and other_slope and degrees(atan(abs((line_slope - other_slope) / float(1 + line_slope * other_slope)))) <= self.MAX_ANGLE_ERROR_DEGREES) or (not line_slope) or (not other_slope)

    def calculate_line_cartesian(self, latitude, longitude):
        point = GPSPoint(latitude, longitude)
        return self.calculate_point_cartesian(point)

    # calculate point cartesian relative to lon1, lat1
    def calculate_point_cartesian(self, point):

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [self.lon1, self.lat1, point.longitude, point.latitude])
        delta_lat = lat2-lat1
        delta_lon = lon2-lon1

        x = delta_lon * cos((lat1+lat2)/2.0) * self.R
        y = delta_lat * self.R
        d = sqrt(x**2 + y**2)

        return x, y, d

    # calculates point_line_distance in meters
    def point_line_distance(self, point):
        x, y, d = self.calculate_point_cartesian(point)
        return abs(x * self.y - self.x * y) / sqrt(self.x ** 2 + self.y ** 2)

    # check if this GPSLine contains a point
    def contains(self, point):
        point_line_distance = self.point_line_distance(point)
        if point_line_distance <= self.MAX_ERROR_DISTANCE and self.lat1 <= point.latitude <= self.lat2:
            return True
        else:
            return False

