import random
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdate

from NormalizationUtils import *

def generate_workload_by_point_dataset(input_path, output_path, lon_width, lat_width, time_width, sample_rate = 0.2):
    """
    generate one specific query workload
    :param input_path: point dataset path
    :param output_path:  generated workload output;
    query_string: format -> "-73.920000, -73.910000, 40.762000,40.772000, timestamp1, timestamp2"
    -73.953418,-73.94341800000001,40.71959,40.72959,1262275200.0,1262278800.0
    :param sample_rate:
    :param lon_width:
    :param lat_width:
    :param time_width: min
    :return:
    """
    file_fd = open(input_path, 'r')

    line = file_fd.readline()
    count = 1

    batch_lines = []
    batch_size = 8192
    while line:

        # if count > 2957579:
        #     # one week
        #     break

        print("current count in the workload: " + str(count))
        items = line.strip().split(',')

        pickup_time_string = items[2].strip()
        pickup_longitude = float(items[5].strip())
        pickup_latitude = float(items[6].strip())
        pickup_timestamp = normalize_date(pickup_time_string)
        pickup_date = datetime.datetime.fromtimestamp(pickup_timestamp)

        random_value = random.random()
        output_line = ""
        if (random_value > (1 - sample_rate)):
            longitude_lower = pickup_longitude - lon_width / 2.0
            longitude_upper = pickup_longitude + lon_width / 2.0
            latitude_lower = pickup_latitude - lat_width / 2.0
            latitude_upper = pickup_latitude + lat_width / 2.0
            date_lower = pickup_date
            date_upper = pickup_date + datetime.timedelta(minutes=time_width)
            output_line = "%s,%s,%s,%s,%s,%s\n" % (longitude_lower, longitude_upper, latitude_lower, latitude_upper, date_lower.timestamp(), date_upper.timestamp())


        print(output_line)
        count = count + 1
        batch_lines.append(output_line)

        if count % batch_size == 0:
            with open(output_path, mode='a') as output_fd:
                output_fd.writelines(batch_lines)
            batch_lines.clear()

        line = file_fd.readline()

    with open(output_path, mode='a') as output_fd:
        output_fd.writelines(batch_lines)

def generate_query_frequency_per_region(input_path, time_interval, spatial_interval, longitude_min, longitude_max, latitude_min, latitude_max, timestamp_min, timestamp_max):
    """
    generate frequency result for one specific query workload
    :param input_path: workload file path (only contains one kind of query workload)
    :param time_interval: second
    :param spatial_interval: float
    :param longitude_min:
    :param longitude_max:
    :param latitude_min:
    :param latitude_max:
    :param timestamp_min:
    :param timestamp_max:
    :return:
    """
    longitude_len = int((longitude_max - longitude_min) / spatial_interval + 1)
    latitude_len = int((latitude_max - latitude_min) / spatial_interval + 1)
    time_len = int((timestamp_max - timestamp_min) / time_interval + 1)
    frequency_result = np.zeros((time_len, longitude_len, latitude_len))

    file_fd = open(input_path, 'r')
    line = file_fd.readline()

    count = 1
    while line:
        print("current count when generating frequency: " + str(count))
        items = line.strip().split(',')
        # longitude_lower = float(items[0])
        # longitude_upper = float(items[1])
        # latitude_lower = float(items[2])
        # latitude_upper = float(items[3])
        # date_lower = float(items[4])
        # date_upper = float(items[5])
        # new record format: 2010-01-01 00:18:01,2009-12-31 00:18:01,2009-12-31 01:18:01,-74.074684,-73.574684,40.477577,40.977577
        longitude_lower = float(items[3])
        longitude_upper = float(items[4])
        latitude_lower = float(items[5])
        latitude_upper = float(items[6])
        date_lower = float(normalize_to_utc_date(items[1]))
        date_upper = float(normalize_to_utc_date(items[2]))
        count += 1

        if (longitude_lower >= longitude_min
        and longitude_upper <= longitude_max
        and latitude_lower >= latitude_min
        and latitude_upper <= latitude_max
        and date_lower >= timestamp_min
        and date_upper <= timestamp_max):

            temporal_start_index = int((date_lower - timestamp_min) / time_interval)
            temporal_stop_index = int((date_upper - timestamp_min) / time_interval)
            longitude_start_index = int((longitude_lower - longitude_min) / spatial_interval)
            longitude_stop_index = int((longitude_upper - longitude_min) / spatial_interval)
            latitude_start_index = int((latitude_lower - latitude_min) / spatial_interval)
            latitude_stop_index = int((latitude_upper - latitude_min) / spatial_interval)

            for i in range(int(temporal_stop_index - temporal_start_index + 1)):
                for j in range(int(longitude_stop_index - longitude_start_index + 1)):
                    for k in range(int(latitude_stop_index - latitude_start_index + 1)):
                        frequency_result[temporal_start_index + i, longitude_start_index + j, latitude_start_index + k] += 1

        line = file_fd.readline()

    return frequency_result


def generate_time_precedence_query_workload(input_path, config_map):
    """
    at this stage, two different regions has different pattern
    :param input_path:
    :param config_map: ['time_precedence_workload_pattern_1.csv'] = [0.01, 0.01, 60]
    :return:
    """

    #generate_workload_by_point_dataset(input_path, "time_precedence_workload_pattern_1.csv", 0.01, 0.01, 60)
    #generate_workload_by_point_dataset(input_path, "time_precedence_workload_pattern_2.csv", 0.1, 0.1, 60)
    for key in config_map.keys():
        config_param_list = config_map.get(key)
        generate_workload_by_point_dataset(input_path, key, config_param_list[0], config_param_list[1], config_param_list[2], config_param_list[3])

    print("finish time-precedence query workload")

def generate_frequency_result_for_time_precedence_query_workload(config_map, time_interval, spatial_interval):
    """

    :param config_map:
    :param time_interval:
    :param spatial_interval:
    :return:
    """
    frequency_result = {}

    for key in config_map.keys():
        region_param_list = config_map.get(key)
        lon_min = region_param_list[4]
        lon_max = region_param_list[5]
        lat_min = region_param_list[6]
        lat_max = region_param_list[7]
        time_min = normalize_to_utc_date(region_param_list[8])
        time_max = normalize_to_utc_date(region_param_list[9])
        frequency_result[key] = generate_query_frequency_per_region(key, time_interval, spatial_interval, lon_min, lon_max, lat_min, lat_max, time_min, time_max)

    print("finish frequency result for query")
    return frequency_result



from HBaseDriver import *

def put_to_hbase(table, frequency_result_map, spatial_interval, longitude_min, latitude_min, time_min):
    """
    hbase table schema

    rowkey = longitude_offset,latitude_offset,day_offset
    column family = workload type
    qualifier = hour offset
    value = frequency value

    time unit is hour in our prediction model

    :param frequency: map: key -> workload name, value -> frequency values (3d array)
    :param time_interval: unit is hour
    :param spatial_interval:
    :param longitude_min:
    :param longitude_max:
    :param latitude_min:
    :param latitude_max:
    :param timestamp_min:
    :param timestamp_max:
    :return:
    """

    hbase_put_datas = dict()

    count = 0
    batch_size = 1024

    connection = happybase.Connection('127.0.0.1')
    for key in frequency_result_map.keys():
        frequency_result = frequency_result_map.get(key)

        normalized_longitude_width = get_normalized_longitude_width(spatial_interval)
        normalized_latitude_width = get_normalized_latitude_width(spatial_interval)

        normalized_longitude_min = normalize_longitude(longitude_min)
        normalized_latitude_min = normalize_latitude(latitude_min)
        normalized_timestamp_min = normalize_to_utc_date(time_min)

        longitude_offset_min = math.floor(normalized_longitude_min / normalized_longitude_width)
        latitude_offset_min = math.floor(normalized_latitude_min / normalized_latitude_width)
        timestamp_hour_offset_min = get_hour_offset(normalized_timestamp_min)

        for time_index, time_item in enumerate(frequency_result):
            for lon_index, lon_item in enumerate(time_item):
                for lat_index, frequency in enumerate(lon_item):
                    longitude_offset = longitude_offset_min + lon_index
                    latitude_offset = latitude_offset_min + lat_index
                    timestamp_hour_offset = timestamp_hour_offset_min + time_index
                    timestamp_day_offset = math.floor(timestamp_hour_offset / 24)

                    rowkey = str(longitude_offset) + "," + str(latitude_offset) + "," + str(timestamp_day_offset)
                    cf_name = key.split(".")[0].split("/")[1]
                    cf_qualifier = cf_name + ":" + str(timestamp_hour_offset - timestamp_day_offset * 24)
                    #print(timestamp_hour_offset - timestamp_day_offset * 24)

                    if rowkey not in hbase_put_datas:
                        hbase_put_datas[rowkey] = {cf_qualifier: str(frequency)}
                    else:
                        hbase_put_datas[rowkey].update({cf_qualifier: str(frequency)})
                    count = count + 1
                    if (count % batch_size == 0):
                        put_batch(hbase_put_datas, connection, table)
                        hbase_put_datas.clear()

    print(count)

    #create_table(connection, "prediction_frequency_test", "workload_1_next_passenger_sample")
    put_batch(hbase_put_datas, connection, table)
    print()


def new_test():
    time_interval = 60 * 60  # 1hour
    spatial_interval = 0.02

    time_precedence_query_config_map = {}
    time_precedence_query_config_map['workload/workload_2_heatmap_airport.csv'] = [0.05, 0.05, 60, 0.2,
                                                                                         -74.05, -73.75, 40.60, 40.90,
                                                                                           "2010-01-01 00:00:00",
                                                                                           "2010-01-31 00:00:00"]

    result = generate_frequency_result_for_time_precedence_query_workload(time_precedence_query_config_map,
                                                                          time_interval, spatial_interval)

    for key in time_precedence_query_config_map.keys():
        frequency_result = result.get(key)

        print(key)
        print(frequency_result.shape)
        interval_len = len(frequency_result)
        x_values = np.arange(0, interval_len, 1)

        s, w, h = frequency_result.shape
        for m in range(w - 1):
            for n in range(h - 1):
                draw_plot(x_values, frequency_result[:, m:m + 1, n:n + 1].reshape(-1))


def test_put_for_real(table):
    time_interval = 60 * 60  # 1hour
    spatial_interval = 0.02

    time_precedence_query_config_map = {}
    time_precedence_query_config_map['workload/workload_1_next_passenger.csv'] = [0.05, 0.05, 60, 0.2,
                                                                                         -74.05, -73.75, 40.60, 40.90,
                                                                                         "2010-01-01 00:00:00",
                                                                                         "2010-01-31 23:59:59"]
    time_precedence_query_config_map['workload/workload_2_heatmap_multiple_5x.csv'] = [0.05, 0.05, 60, 0.2,
                                                                                                 -74.05, -73.75, 40.60,
                                                                                                 40.90,
                                                                                                 "2010-01-01 00:00:00",
                                                                                                 "2010-01-31 23:59:59"]

    result = generate_frequency_result_for_time_precedence_query_workload(time_precedence_query_config_map,
                                                                          time_interval, spatial_interval)

    print()
    put_to_hbase(table, result, spatial_interval, -74.05, 40.60, "2010-01-01 00:00:00")


def test_put_for_predicted(table):
    time_interval = 60 * 60  # 1hour
    spatial_interval = 0.02

    time_precedence_query_config_map = {}

    time_precedence_query_config_map['workload/workload_2_heatmap_multiple.csv'] = [0.05, 0.05, 60, 0.2,
                                                                                    -74.05, -73.75, 40.60,
                                                                                    40.90,
                                                                                    "2010-01-22 00:00:00",
                                                                                    "2010-01-29 23:59:59"]

    result = generate_frequency_result_for_time_precedence_query_workload(time_precedence_query_config_map,
                                                                          time_interval, spatial_interval)

    print()
    put_to_hbase(table, result, spatial_interval, -74.05, 40.60, "2010-01-22 00:00:00")


if __name__ == "__main__":
    table = "frequency_real_test_month1_workload_multiple_ratio-12-5"
    #create_table_with_2cf(connection, table, "workload_1_next_passenger", "workload_2_heatmap_multiple")
    test_put_for_real(table)


