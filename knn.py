'''K nearest neighbor classification method'''
from __future__ import division
import operator
import argparse
import csv
import math


class NearestNeighbors:
    '''Class saves k-nearest neighbors out of many for specific point'''
    def __init__(self, center, k):
        self.k = k
        self.center = center
        self.neighbors = list()  # [point, dist]

    def append(self, point):
        dist = self.__euclidian_dist(point)
        self.neighbors.append([point, dist])
        self.neighbors = sorted(self.neighbors, key=operator.itemgetter(1))
        del self.neighbors[self.k:]

    def get_class(self):
        point_class = dict()

        for neighbor in self.neighbors:
            if neighbor[0][-1] not in point_class.keys():
                point_class.update({neighbor[0][-1]: 1})
            else:
                point_class[neighbor[0][-1]] += 1
        print point_class.keys()
        return max(point_class.iteritems(), key=operator.itemgetter(1))[0]

    def __euclidian_dist(self, point):
        result = 0
        for i in xrange(len(self.center)-1):
            result += (float(self.center[i]) - float(point[i])) ** 2
        return math.sqrt(result)

    def print_closest_neighbors(self):
        print 'Closest neighbor'
        for neighbor in self.neighbors:
            print neighbor


def get_accuracy():
    pass


def load(filename):
    with open(filename) as file:
        data = csv.reader(file, delimiter=',')
        data = [row for row in data]
        return data


def knn(t_data, c_data, k):
    for cpoint in c_data:
        nn = NearestNeighbors(cpoint, k)
        [nn.append(tpoint) for tpoint in t_data]
        nn.print_closest_neighbors()
        print 'Point class: {}'.format(nn.get_class())
        print '---------------'


def parse_options():
    optparser = argparse.ArgumentParser(description='K-NN Algorithm.')
    optparser.add_argument(
        '-ft', '--input_file_training',
        dest='tfile',
        help='filename containing csv for training',
        required=True
    )
    optparser.add_argument(
        '-fc', '--input_file_classification',
        dest='cfile',
        help='filename containing csv for classification',
        required=True
    )
    optparser.add_argument(
        '-k', '--neighbors',
        dest='neighbors',
        help='number of neighbors',
        default=5,
        type=int
    )
    return optparser.parse_args()


options = parse_options()
t_data = load(options.tfile)  # training data
c_data = load(options.cfile)  # classifying data
knn(t_data, c_data, options.neighbors)


get_accuracy()