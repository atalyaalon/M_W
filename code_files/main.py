from code_files.RoadMap import RoadMap
from code_files.DrivingSession import DrivingSession
import os
import csv

gpx_file_path = '..\\data\\road6'
gpx_file_name = 'mapstogpx_road6_South_to_North.gpx'
driving_sessions_file_path = '..\\data\\sessions'
output_file_path = '..\\output'


if __name__ == "__main__":

    road6_map = RoadMap(os.path.join(gpx_file_path, gpx_file_name))

    # process driving sessions
    driving_sessions = []
    for file_name in os.listdir(driving_sessions_file_path):
        curr_driving_session = DrivingSession(os.path.join(driving_sessions_file_path, file_name))
        driving_sessions.append(curr_driving_session)
        # add samples of session to road segments
        road6_map.add_session_samples_to_road_segments(curr_driving_session)

    # create output dir if necessary
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)

    # calculate slopes and save data
    with open(os.path.join(output_file_path, 'slopes.csv'), 'wt', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['latitude_1', 'longitude_1', 'latitude_2', 'longitude_2', 'slope_in_percentage', 'slope_standard_deviation_in_percentage'])
        for road_segment in road6_map.road_segments:
            road_segment.calculate_slope()
            writer.writerow([road_segment.line.lat1, road_segment.line.lon1, road_segment.line.lat2, road_segment.line.lon2,
                             road_segment.slope_in_percentage, road_segment.slope_standard_deviation_in_percentage])
