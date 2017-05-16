from statistics import mean, stdev
from code_files.GPSLine import GPSLine


class RoadSegment:

    def __init__(self, point_a, point_b):
        self.line = GPSLine(point_a, point_b)
        self.slope_in_percentage = None
        self.slope_standard_deviation_in_percentage = None
        self.slopes_list_in_percentages = []
        self.samples_lists = []

        # constants
        self.POWER = 0.19
        self.ROOM_TEMPERATURE_KELVIN = 298.15 # assuming room temperature during the whole ride - not exact
        self.PRESSURE_AT_SEA_LEVEL = 101325.0
        self.STANDARD_TEMP_LAPSE_RATE_ABS = 0.0065

    def add_samples_list(self, samples_list):
        if samples_list:
            self.samples_lists.append(samples_list)

    def calculate_slope(self):
        if self.samples_lists:
            for samples_list in self.samples_lists:
                distance_delta = 0
                for sample in samples_list[1:]: distance_delta += sample.distance_delta_from_last_sample
                height_delta = self.hyposometric_formula(samples_list[len(samples_list)-1].pressure) - self.hyposometric_formula(samples_list[0].pressure) # in meters
                curr_slope_in_percentage = 100 * height_delta / float(distance_delta)
                self.slopes_list_in_percentages.append(curr_slope_in_percentage)

            self.slope_in_percentage = mean(self.slopes_list_in_percentages)
            if len(self.samples_lists) > 1:
                self.slope_standard_deviation_in_percentage = stdev(self.slopes_list_in_percentages)

    # given the current atmospheric pressure in pasal units, returns the current height in meters.
    # Assumes room temperature during the whole ride - not exact
    def hyposometric_formula(self, pressure):
        return ((((self.PRESSURE_AT_SEA_LEVEL/pressure)**self.POWER) - 1)*self.ROOM_TEMPERATURE_KELVIN)/self.STANDARD_TEMP_LAPSE_RATE_ABS

    def contains(self,sample):
        if self.line.contains(sample.gps_point):
            return True
        else:
            return False
    # verify that the current sample belongs to segment and not to a road segment near by (can happen in an interchange)
    def samples_belong_to_segment(self, samples):
        return self.lines_slope_signs_similar(samples) and self.angle_between_lines_is_appropriate(samples)

    # check if the RoadSegment's GPLLine slopes have the same sign to samples GPSLine
    # (meaning the samples are on the road and not above / below it due to an interchange or junction)
    def lines_slope_signs_similar(self, samples):
        samples_line = GPSLine(samples[0].gps_point, samples[len(samples)-1].gps_point)
        return self.line.lines_slope_signs_similar(samples_line)

    # check if the angle between RoadSegment's GPLLine and and samples GPSLine is smaller than the threshold self.MAX_ANGLE_ERROR_DEGREES
    def angle_between_lines_is_appropriate(self, samples):
        samples_line = GPSLine(samples[0].gps_point, samples[len(samples)-1].gps_point)
        return self.line.angle_between_lines_is_appropriate(samples_line)