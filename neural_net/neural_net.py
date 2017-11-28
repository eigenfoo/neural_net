'''
neural_net.py
'''

from math import trunc
import numpy as np


def read_neural_net_file(filename):
    ''' Reads neural net file'''
    with open(filename, 'r') as infile:
        line = infile.readline()
        nums = [int(num) for num in line.split()]
        num_input, num_hidden, num_output = nums

        weights1 = np.zeros([num_hidden, num_input+1])
        for i in range(num_hidden):
            line = infile.readline()
            nums = [float(num) for num in line.split()]
            weights1[i, :] = nums

        weights2 = np.zeros([num_output, num_hidden+1])
        for i in range(num_output):
            line = infile.readline()
            nums = [float(num) for num in line.split()]
            weights2[i, :] = nums

    return num_input, num_hidden, num_output, [weights1, weights2]


def read_data_file(filename):
    ''' Reads data file'''
    with open(filename, 'r') as infile:
        line = infile.readline()
        nums = [int(num) for num in line.split()]
        num_obs, num_input, num_output = nums

        inputs = np.zeros([num_obs, num_input])
        outputs = np.zeros([num_obs, num_output])

        for i in range(num_obs):
            line = infile.readline()
            nums = [float(num) for num in line.split()]
            inputs[i, :] = nums[:num_input]
            outputs[i, :] = nums[num_input:]

    return list(zip(inputs, outputs))


def write_trained_file(filename, num_input, num_hidden, num_output, weights):
    ''' Writes trained neural net '''
    with open(filename, 'w') as outfile:
        print(' '.join(str(n) for n in [num_input, num_hidden, num_output]),
              file=outfile)
        for i in range(num_hidden):
            print(' '.join('{:.3f}'.format(j) for j in weights[0][i, :]),
                  file=outfile)
        for i in range(num_output):
            print(' '.join('{:.3f}'.format(j) for j in weights[1][i, :]),
                  file=outfile)


def write_results_file(filename, num_output, confusion):
    ''' Writes results file '''
    accuracies = []
    precisions = []
    recalls = []
    f1s = []

    with open(filename, 'w') as outfile:
        for i in range(num_output):
            accuracies.append((confusion[i, 0, 0] + confusion[i, 1, 1])
                              / confusion[i].sum())
            precisions.append(confusion[i, 0, 0] / confusion[i, 0, :].sum())
            recalls.append(confusion[i, 0, 0] / confusion[i, :, 0].sum())
            f1s.append(2*precisions[-1]*recalls[-1]
                       / (precisions[-1] + recalls[-1]))

            print(' '.join('{:d}'.format(trunc(j))
                           for j in confusion[i].flatten()),
                  end=' ', file=outfile)
            print(' '.join('{:.3f}'.format(j)
                           for j in [accuracies[-1], precisions[-1],
                                     recalls[-1], f1s[-1]]),
                  file=outfile)

        micro_confusion = confusion.sum(axis=0)
        micro_accuracy = (micro_confusion[0, 0] + micro_confusion[1, 1]) \
            / micro_confusion.sum()
        micro_precision = micro_confusion[0, 0] / micro_confusion[0, :].sum()
        micro_recall = micro_confusion[0, 0] / micro_confusion[:, 0].sum()
        micro_f1 = (2*micro_precision*micro_recall) \
            / (micro_precision + micro_recall)

        print(' '.join('{:.3f}'.format(j)
                       for j in [micro_accuracy, micro_precision,
                                 micro_recall, micro_f1]),
              file=outfile)

        macro_accuracy = sum(accuracies) / len(accuracies)
        macro_precision = sum(precisions) / len(precisions)
        macro_recall = sum(recalls) / len(recalls)
        macro_f1 = (2*macro_precision*macro_recall) \
            / (macro_precision + macro_recall)

        print(' '.join('{:.3f}'.format(j)
                       for j in [macro_accuracy, macro_precision,
                                 macro_recall, macro_f1]),
              file=outfile)


def train(num_input, num_hidden, num_output, weights, training_data):
    ''' Trains neural network '''
    pass


def test(num_output, weights, test_data):
    ''' Tests neural network '''
    confusion = np.zeros([num_output, 2, 2])

    for inputs, outputs in test_data:
        predicted = np.around(feedforward(inputs, weights))

        for i in range(num_output):
            if predicted[i] == 1 and outputs[i] == 1:
                confusion[i, 0, 0] += 1
            elif predicted[i] == 1 and outputs[i] == 0:
                confusion[i, 0, 1] += 1
            elif predicted[i] == 0 and outputs[i] == 1:
                confusion[i, 1, 0] += 1
            elif predicted[i] == 0 and outputs[i] == 0:
                confusion[i, 1, 1] += 1

    return confusion


def sigmoid(vals):
    ''' The sigmoid function '''
    return 1.0 / (1.0 + np.exp(-vals))


def sigmoid_prime(vals):
    ''' Derivative of the sigmoid function '''
    return sigmoid(vals) * (1-sigmoid(vals))


def feedforward(inputs, weights):
    ''' Return the output of the network if `inputs` is input '''
    activation = inputs
    for weight in weights:
        activation = np.insert(activation, 0, -1)
        activation = sigmoid(np.dot(weight, activation))
    return activation
