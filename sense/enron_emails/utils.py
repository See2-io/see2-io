# Django modules.

# Third party modules.
import json
import os


# See2-io modules.
from sense.models import ADataFilter
from sense.settings import ENRON_SIM_PERIOD, ENRON_DATA_SIM


class FilteredDataSetsCache:
    '''
    A :class: used to cache Enron email datasets during the simulation and occasionally write to file.
    '''
    def __init__(self, name):
        self.filtered_dataset_caches = {}
        self.data_filters = ADataFilter.objects.filter(dataset__name=name)
        for data_filter in self.data_filters:
            self.filtered_dataset_caches[data_filter.name] = {
                'Name': data_filter.name,
                'Cache': [],
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
            item = {
                'id': data.id,
                'cc': data.cc,
                'datetime': data.datetime.strftime('%y-%m-%d %H:%M:%S'),
                'bcc': data.bcc,
                'sender': data.sender,
                'recipients': data.recipients,
                'subject': data.subject,
                'body': data.body,
            }
            self.filtered_dataset_caches[name]['Cache'].append(item)

    def get_filtered_data_cache(self, name):
        '''

        :return:
        '''
        if name in self.filtered_dataset_caches.keys():
            return self.filtered_dataset_caches[name]
        else:
            return None

    def write_to_file(self, sim_time):
        '''

        :return: Nothing
        '''
        json_data = {
            'ENRON_SIM_PERIOD': sim_time - ENRON_SIM_PERIOD,
            'Caches': self.filtered_dataset_caches,
        }
        fp = os.path.join(ENRON_DATA_SIM, 'enron_filtered_datasets.json')
        with open(fp, 'a') as f:
            json.dump(json_data, f, indent=4)
            f.close()
