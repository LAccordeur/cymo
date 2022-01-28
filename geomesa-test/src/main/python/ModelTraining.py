import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import torch.utils.data as data
import matplotlib.pyplot as plt

from CNNLSTMHybridModel import LSTMCombineCNN
from TypicalQueryWorkloadGenerator import generate_frequency_result_for_time_precedence_query_workload
from TypicalQueryWorkloadGenerator import generate_time_precedence_query_workload
from TrainingDatasetHandler import create_inout_sequences_from_multiple_workloads
from TrainingDatasetHandler import search_max_frequency_of_workload
from ModelEvaluation import evaluate

# training setting
LOCAL_LENGTH = 5
SEQ_LENGTH = 12

class Args:
    def __init__(self):
        self.cuda = True
        self.no_cuda = False
        self.seed = 1
        self.batch_size = 50
        self.test_batch_size = 1000
        self.epochs = 250
        self.lr = 0.001
        self.momentum = 0.5
        self.log_interval = 10


class FrequncyImageDataset(data.Dataset):

    def __init__(self, frequency_data, transform=None):
        self.transform = transform

        self.data = []
        self.labels = []
        for i in range(len(frequency_data)):
            frequency_seq = frequency_data[i][0]
            label = frequency_data[i][1]
            self.data.append(frequency_seq)
            self.labels.append(label)

        self.data = np.array(self.data)
        self.labels = np.array(self.labels)
        self.tensor_data = torch.from_numpy(np.expand_dims(self.data, axis=2))


    def __getitem__(self, index):
        data_item = self.tensor_data[index]
        data_label = self.labels[index]
        if self.transform:
            data_item = self.transform(data_item)
        return (data_item, data_label)

    def __len__(self):
        return len(self.data)


args = Args()
args.cuda = not args.no_cuda and torch.cuda.is_available()
print("cuda: " + str(args.cuda))

torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)
kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}


model = LSTMCombineCNN(local_len=LOCAL_LENGTH)
if args.cuda:
    model.cuda()

optimizer = optim.Adam(model.parameters(), lr=args.lr)
loss_function = nn.MSELoss()


def train(epoch, train_loader):
    model.train()

    for batch_idx, (data, target) in enumerate(train_loader, 0):

        #data = torch.FloatTensor(data)
        if args.cuda:
            data, target = data.cuda(), target.cuda()

        target = torch.tensor(target, dtype=torch.float32)
        data = torch.tensor(data, dtype=torch.float32)
        #data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = model(data)

        loss = loss_function(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))


def execute_training():
    time_interval = 60 * 60  # 1hour
    spatial_interval = 0.02
    training_dataset_len = 24 * 21

    time_precedence_query_config_map = {}

    time_precedence_query_config_map['workload/workload_1_next_passenger.csv'] = [0.01, 0.01, 60, 0.2, -74.05, -73.75, 40.60, 40.90,
                                                                                           "2010-01-01 00:00:00",
                                                                                           "2010-01-29 00:00:00"]
    frequency_result = generate_frequency_result_for_time_precedence_query_workload(time_precedence_query_config_map,time_interval, spatial_interval)
    normalization_coff = search_max_frequency_of_workload(frequency_result)

    training_inout_seq_normalized = create_inout_sequences_from_multiple_workloads(frequency_result, SEQ_LENGTH, LOCAL_LENGTH, training_dataset_len, normalization_coff)
    training_dataset = FrequncyImageDataset(training_inout_seq_normalized)
    training_loader = torch.utils.data.DataLoader(training_dataset, batch_size=args.batch_size, shuffle=True, num_workers=1)

    for epoch in range(1, args.epochs + 1):
        train(epoch, training_loader)

    torch.save(model, "cnn_lstm_test.model")
    print("saved model")



if __name__ == '__main__':

    execute_training()


