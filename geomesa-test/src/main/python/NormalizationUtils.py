import time
import datetime
import math

SPATIAL_NORMALIZE_PRECISION = 21

def normalize_latitude(latitude):
    min = -90
    max = 90
    bins = 1 << SPATIAL_NORMALIZE_PRECISION
    normalizer = bins / (max - min)
    maxIndex = int(bins - 1)

    if (latitude >= max):
        return maxIndex
    else:
        return int(math.floor((latitude - min) * normalizer))

    print("")

def normalize_longitude(longitude):
    min = -180
    max = 180

    bins = 1 << SPATIAL_NORMALIZE_PRECISION
    normalizer = bins / (max - min)
    maxIndex = int(bins - 1)

    if (longitude >= max):
        return maxIndex
    else:
        return int(math.floor((longitude - min) * normalizer))
    print("")

def get_normalized_latitude_width(spatial_width):
    min = -90
    max = 90
    bins = 1 << SPATIAL_NORMALIZE_PRECISION
    normalizer = bins / (max - min)

    return math.floor(normalizer * spatial_width)

def get_normalized_longitude_width(spatial_width):
    min = -180
    max = 180

    bins = 1 << SPATIAL_NORMALIZE_PRECISION
    normalizer = bins / (max - min)
    return math.floor(normalizer * spatial_width)


def normalize_to_utc_date(date_string):
    """

    :param date_string:
    :return: epoch second (different from java)
    """
    time_array = time.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(time_array)
    print("")

    #utc offset
    epoch_date_offset = 8 * 60 * 60
    return int(timestamp + epoch_date_offset)

def normalize_date(date_string):
    """

    :param date_string:
    :return: epoch second (different from java)
    """
    time_array = time.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(time_array)
    # print("")

    return int(timestamp)

def get_hour_offset(timestamp):
    """

    :param timestamp: epoch second
    :return:
    """
    epoch_hour = timestamp / (60 * 60)
    return math.floor(epoch_hour)



def timestamp_to_hour(timestamp):
    return int(timestamp / (60 * 60))


if __name__ == "__main__":

    #print(normalize_to_utc_date("2010-01-01 00:34:00"))
    print(normalize_longitude(70.1212))
    print(get_normalized_latitude_width(0.05))
    print(normalize_to_utc_date("2011-01-12 15:00:00"))
    print("finish")