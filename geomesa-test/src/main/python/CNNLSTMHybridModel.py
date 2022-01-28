import torch
import torch.nn as nn
import torch.nn.functional as F



class CNN(nn.Module):
    def __init__(self, feature_len = 16, local_len = 5):
        # input: 1xSxS image, assume S = 5
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, feature_len, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(feature_len * local_len * local_len, 64)
        self.fc2 = nn.Linear(64, feature_len)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        batch_size, feature_num, height, width = x.size()
        x = x.view(-1, feature_num*height*width)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class LSTMCombineCNN(nn.Module):
    def __init__(self, feature_len = 16, local_len = 5, output_size = 1):
        super(LSTMCombineCNN, self).__init__()
        self.cnn = CNN(local_len=local_len)
        self.rnn = nn.LSTM(
            input_size=feature_len,
            hidden_size=64*4*2,
            num_layers=1,
            batch_first=True)
        self.linear = nn.Linear(64*4*2, output_size)

    def forward(self, x):
        batch_size, timesteps, C, H, W = x.size()
        c_in = x.view(batch_size * timesteps, C, H, W)
        c_out = self.cnn(c_in)
        r_in = c_out.view(batch_size, timesteps, -1)
        r_out, (h_n, h_c) = self.rnn(r_in)
        # only handle the last output
        r_out2 = self.linear(r_out[:, -1, :])

        return r_out2.view(-1)



