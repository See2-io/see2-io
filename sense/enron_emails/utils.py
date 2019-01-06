# Django modules.

# Third party modules.

# See2-io modules.
from sense.models import ADataFilter


class FilteredDataSetsCache:
    '''
    A :class: used to cache Enron email datasets during the simulation and occasionally write to file.
    '''
    def __init__(self, name):
        self.filtered_dataset_caches = {}
        self.data_filters = ADataFilter.objects.filter(dataset__name=name)
        for data_filter in self.data_filters:
            self.filtered_dataset_caches[data_filter.name] = {
                'Data': [],
                # 'Filter': data_filter.filter,
                # 'Filtered_Dataset': data_filter.filtered_dataset,
                # 'DataSet': data_filter.dataset,
            }

    def get_data_filters(self):
        '''
        Return the set of :class: sense.models.ADataFilters.
        :return: A QuerySet from :class: sense.nodels.ADataFilter.
        '''
        # if not self.data_filters:
        #     self.data_filters = ADataFilter.objects.filter(dataset__name=name)
        return self.data_filters

    def add_data(self, name, data):
        '''

        :param name:
        :return:
        '''
        if name in self.filtered_dataset_caches.keys():
            self.filtered_dataset_caches[name]['Data'].append(data)

    def get_filtered_data_cache(self, name):
        '''

        :return:
        '''
        if name in self.filtered_dataset_caches.keys():
            return self.filtered_dataset_caches[name]
        else:
            return None
