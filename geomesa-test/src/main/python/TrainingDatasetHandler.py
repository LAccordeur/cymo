import numpy as np
import matplotlib.pyplot as plt


def create_inout_sequences(input_data, seq_length, local_region_length):
    """
    create train data set
    :param input_data: a list of frequency image num x H x W
    :param seq_length:
    :return: a list, the element has this format: SxS local image list -> target (next frequency)
    """
    print("begin create dataset")
    padding_len = int(local_region_length / 2)
    # padding input_data
    image_padding = np.pad(input_data, ((0, 0), (padding_len, padding_len), (padding_len, padding_len)), 'constant', constant_values=(0, 0))

    inout_seq = []
    n, h, w = input_data.shape
    for n_i in range(n - seq_length):
        print(n_i)
        for h_i in range(h):
            for w_i in range(w):
                train_seq = image_padding[n_i:n_i+seq_length,h_i:h_i+local_region_length, w_i:w_i+local_region_length]
                train_label = input_data[n_i+seq_length, h_i, w_i]
                inout_seq.append((train_seq, train_label))

    return inout_seq

def create_inout_sequences_from_multiple_workloads(input_workload_map, seq_length, local_region_length, training_dataset_length, normalization_coff):
    """

    :param input_workload_map:
    :param seq_length:
    :param local_region_length:
    :return:
    """

    total_inout_seq = []
    for value in input_workload_map.values():
        normalized_value = value[0: training_dataset_length] * 1.0 / normalization_coff
        total_inout_seq.extend(create_inout_sequences(normalized_value, seq_length, local_region_length))

    return total_inout_seq

def search_max_frequency_of_workload(input_workload_map):
    max_frequency = 0
    for value in input_workload_map.values():
        current_max_value = value.max()
        if (current_max_value > max_frequency):
            max_frequency = current_max_value

    return max_frequency












