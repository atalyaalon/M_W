import gpxpy
import gpxpy.gpx
from code_files.RoadSegment import RoadSegment
from code_files.HelperFunctions import HelperFunctions
from code_files.GPSPoint import GPSPoint


class RoadMap:

    def __init__(self, gpx_file_name):
        self.gpx_file_name = gpx_file_name
        self.road_segments = []
        self.road_points = []
        self.parse_gpx_file()

    def add_segment(self, road_segment):
        self.road_segments.append(road_segment)

    def parse_gpx_file(self):
        gpx_file = open(self.gpx_file_name, 'r')
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                self.road_points += segment.points
                for point_a, point_b in HelperFunctions.pairwise(segment.points):
                    road_segment = RoadSegment(GPSPoint(point_a.latitude, point_a.longitude), GPSPoint(point_b.latitude, point_b.longitude))
                    self.add_segment(road_segment)

    def search_idx_by_route_order(self, sample, first_idx, last_idx=None):
        if last_idx is None:
            index = self.binary_search_in_route(sample, first_idx)
        else:
            index = self.regular_search_in_route(sample, first_idx, last_idx)
        if index is not None:
            return index
        return None

    def binary_search_in_route(self, sample, first_idx):
        first = first_idx
        last = len(self.road_segments)-1
        while first <= last:
            midpoint = (first + last)//2
            if self.road_segments[midpoint].contains(sample):
                return midpoint
            else:
                if sample.gps_point.latitude < self.road_segments[midpoint].line.lat1:
                    last = midpoint-1
                else:
                    first = midpoint+1
        return None

    def regular_search_in_route(self, sample, first_idx, last_idx):
        for curr_index in range(first_idx, last_idx + 1):
            if self.road_segments[curr_index].contains(sample):
                return curr_index
        return None

    def get_curr_road_segment_idx_of_sample(self, prev_road_segment_idx, sample):
        # if prev index is None, search sample in all map
        if prev_road_segment_idx is None:
            curr_road_segment_idx = self.search_idx_by_route_order(sample, 0)
        else:   # else prev index has value, search sample in the segment of prev_index and in the following 10 indices only
            curr_road_segment_idx = self.search_idx_by_route_order(sample, prev_road_segment_idx, min(prev_road_segment_idx + 3, len(self.road_segments)-1))
        return curr_road_segment_idx

    def add_session_samples_to_road_segments(self, curr_driving_session):
        samples_list_of_curr_road_segment = []
        prev_road_segment_idx = None
        for sample in curr_driving_session.samples:
            curr_road_segment_idx = self.get_curr_road_segment_idx_of_sample(prev_road_segment_idx, sample)
            # if sample wasn't found on road 6, or it was found and segment was changed relative to previous segment (previous segment idx might have been None)
            if curr_road_segment_idx is None or curr_road_segment_idx != prev_road_segment_idx:
                # if there is more than two samples in samples_list_of_curr_road_segment
                # and the sample belongs to current road segment and not to a road segment near by (can happen in an interchange)
                if len(samples_list_of_curr_road_segment) > 2 and self.road_segments[prev_road_segment_idx].samples_belong_to_segment(samples_list_of_curr_road_segment):
                    self.road_segments[prev_road_segment_idx].add_samples_list(samples_list_of_curr_road_segment)
                samples_list_of_curr_road_segment = []  # empty list
                if curr_road_segment_idx:   # if current index is not None, add sample to samples list
                    samples_list_of_curr_road_segment.append(sample)
            else: # sample was found on road 6 and it's segment's index is identical to the previous index therefore add sample to samples list
                samples_list_of_curr_road_segment.append(sample)
            prev_road_segment_idx = curr_road_segment_idx
