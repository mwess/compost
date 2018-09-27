import math
import random

from compost.utils import NotEnoughArgumentsException, NotIterableError


class KfoldCV:

    def __init__(self, n_splits=None, group_size=None):
        """
        Split data according to either strategy. If both arguments are provided, n_splits take precedence. The
        parameter that is not provided will be computed based on the data to be split.
        :param n_splits: If not None, number of groups in which to split the data.
        :param group_size: If not None, size of each group.
        """
        if n_splits is None and group_size is None:
            raise NotEnoughArgumentsException('Neither n_splits nor group_size was provided.')
        self._n_splits = n_splits
        self._group_size = group_size
        self._data_size = -1
        self._split_initialized = False
        self._idxs = []

    def split(self, data):
        """

        :param data:
        :return:
        """
        if not hasattr(data, '__iter__'):
            raise NotIterableError('Type {} is not iterable.'.format(type(data)))
        self._data_size = len(data)
        self._idxs = list(range(self._data_size))
        random.shuffle(self._idxs)
        if self._n_splits is not None:
            self._group_size = math.ceil(self._data_size/self._n_splits)
        else:
            self._n_splits = math.ceil(self._data_size/self._group_size)

        self._split_initialized = True

    def __iter__(self):
        for i in range(self._n_splits):
            x_idx = self._idxs[i*self._group_size:i*self._group_size + self._group_size]
            y_idx = self._idxs[:i*self._group_size] + self._idxs[i*self._group_size + self._group_size:]
            yield x_idx, y_idx

def compute_performance(tag_res, data):
    # TODO: Make sure the lower solution works before deleting.
    #perf = 0
    #counter = 0
    #for sent_ind in range(len(data)):
    #    for ind in range(len(sent_ind))
    #        counter += 1
    #        if data[sent_ind][ind][1] == tag_res[ind]:
    #            perf += 1
    #return perf/counter
    tag_res_flattened = [tag for sentence in tag_res for tag in sentence]
    data_flattened = [token[1] for sentence in data for token in sentence]
    return sum([x[0] == x[1] for x in zip(tag_res_flattened, data_flattened)])/len(data_flattened)


def kfoldcv_training(taggers, data, options):
    # TODO: Implement saving option for best trained models.
    nsplits = options.opts.get('kfcv_nsplits', None)
    group_size = options.opts.get('kfcv_group_size', None)
    performances = []
    kfcv = KfoldCV(nsplits, group_size)
    kfcv.split(data)
    for test_idx, train_idx in kfcv:
        test_data = list(map(lambda x: data[x], test_idx))
        train_data = list(map(lambda x: data[x], train_idx))
        tmp_performances = {}
        for tagger in taggers:
            tagger.train(train_data)
            test_result = tagger.tag(test_data)
            perf = compute_performance(test_result, test_data)
            tmp_performances[tagger.name] = perf
        performances.append(tmp_performances)
    return performances