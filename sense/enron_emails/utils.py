'''
==============================================================
~sense.enron_emails.utils.py

==============================================================
Utility classes and functions for processing Enron Corporation data.

Author: dave.dyke@see2.io
Licence: TODO
Copyright See2 Limited 2018
'''

# See2-io modules.
from sense.models import ADataFilter
from sense.settings import ENRON_SIM_PERIOD, ENRON_DATA_SIM

# Third party imports
import pandas as pd
import json
from datetime import datetime
import re
import os


class FilteredDataSetsCache:
    '''
    A :class: used to cache Enron email datasets during the simulation and occasionally write to file.
    '''
    def __init__(self, name):
        self.gource = open(os.path.join(ENRON_DATA_SIM, 'enron_sim_gource.log'), 'w')
        self.filtered_dataset_caches = {}
        self.filtered_dataset_caches['Enron God Data Filter'] = {
            'Name': 'Enron God Data Filter',
            'Cache': pd.DataFrame(),
            'Topics': set(),
        }
        self.data_filters = ADataFilter.objects.filter(dataset__name=name)
        for data_filter in self.data_filters:
            self.filtered_dataset_caches[data_filter.name] = {
                'Name': data_filter.name,
                'Cache': pd.DataFrame(),
                'Topics': [],
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
        # Build the email data item
        item = {
            'id': data.id,
            'cc': data.cc,
            'datetime': data.datetime.strftime('%y-%m-%d %H:%M:%S'),
            'bcc': data.bcc,
            'sender': data.sender,
            'recipients': data.recipients,
            'subject': data.subject,
            'body': data.body,
            'clean_body': data.clean_body,
        }
        # Add the item (email) to the 'Enron God' set
        df = self.filtered_dataset_caches['Enron God']['Cache']
        df = df.append(item, ignore_index=True,)
        self.filtered_dataset_caches['Enron God']['Cache'] = df

        # Add item to the named sub-community
        if name in self.filtered_dataset_caches.keys():
            df = self.filtered_dataset_caches[name]['Cache']
            df = df.append(item, ignore_index=True)
            self.filtered_dataset_caches[name]['Cache'] = df
            # Next line prints to stdout for piping in 'realtime' to gource visualisation.
            # print('%d|%s|M|Enron Corporation/%s' % (data.datetime.timestamp(), data.sender[1:-1], name[:-12]))
            self.gource.write('%d|%s|M|Enron Corporation/%s\n' % (data.datetime.timestamp(), data.sender[1:-1], name[:-12]))

            # Touch any topics mentioned in this email
            topics = self.filtered_dataset_caches[name]['Topics']
            for topic in topics:
                if topic in data.clean_body:
                    self.gource.write('%d|%s|M|Enron Corporation/%s/%s\n' % (data.datetime.timestamp(), data.sender[1:-1], name[:-12], topic))

    def get_filtered_data_cache(self, name):
        '''

        :return:
        '''
        if name in self.filtered_dataset_caches.keys():
            return self.filtered_dataset_caches[name]
        else:
            return None

    def get_cache_keys(self):
        '''
        TODO consider making the class iterable over its caches.
        :return:
        '''
        return self.filtered_dataset_caches.keys()

    def process_caches(self, sim_time):
        '''

        :param sim_time:
        :return:
        '''
        for name in self.filtered_dataset_caches.keys():
            cache = self.filtered_dataset_caches[name]
            print(cache['Cache'].shape)

    def update_topics(self, timestamp, name, new_topics):
        '''

        :return:
        '''
        if name in self.filtered_dataset_caches.keys():
            old_topics = set(self.filtered_dataset_caches[name]['Topics'])
            for topic in old_topics.difference(new_topics):
                self.gource.write('%d|Enron God|D|Enron Corporation/%s/%s\n' % (timestamp, name[:-12], topic))
            for topic in old_topics & new_topics:
                self.gource.write('%d|Enron God|M|Enron Corporation/%s/%s\n' % (timestamp, name[:-12], topic))
            for topic in new_topics.difference(old_topics):
                self.gource.write('%d|Enron God|A|Enron Corporation/%s/%s\n' % (timestamp, name[:-12], topic))
            self.filtered_dataset_caches[name]['Topics'] = new_topics

    def write_to_file(self, sim_time):
        '''

        :return: Nothing
        '''
        json_data = {
            'ENRON_SIM_PERIOD': sim_time - ENRON_SIM_PERIOD,
            'Caches': self.filtered_dataset_caches,
        }
        fp = os.path.join(ENRON_DATA_SIM, 'enron_filtered_datasets.json')
        with open(fp, 'w') as f:
            json.dump(json_data, f, indent=4)
            f.close()


def remove_html_markup(markup):
    """
    Removes HTML markup from given 'html'.

    :param markup: the input text with embedded html tags.
    :type markup: str
    :rtype: str
    :return: plain text without html markup.
    """
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", markup.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    # return html2text(cleaned.strip())
    return cleaned.strip()


def clean_email(body):
    """
    Removes unimportant chaff from the body text.

    :param body: the email body text to be cleaned.
    :type body: str
    :rtype: str
    :return: plain text without the chaff.
    """
    clean_text = body.strip()
    # clean_text = re.sub(r'[^\w\s]', ' ', clean_text)
    # clean_text = clean_text.replace('\n', ' ')
    clean_text = clean_text.replace('\r\n', ' ')
    # clean_text = clean_text.replace('\t', ' ')
    #  Remove anything longer than 64 characters
    clean_text = re.sub(r'\w{64,}', ' ', clean_text)
    #  Remove other weird characters like :;/\-_=+{}()[]|~`'"@$%^&*
    clean_text = re.sub(r'[~<>\"\-_\*\+=\|\(\)\{\}\[\]\r\n\t]+', ' ', clean_text)
    # clean_text = re.sub(r'[~\?!<>\"\-_\*,;\+=\|\(\)\{\}\[\]\\\r\n\t]+', ' ', clean_text)
    clean_text = ' '.join(re.split("\s+", clean_text, flags=re.UNICODE))
    clean_text = clean_text.strip()
    # clean_text = clean_text.replace('  ', ' ')
    # Remove numbers, e.g 123
    # cleaned = re.sub(r"\d+", "", text.strip())

    # Remove unhelpful punctuation
    clean_text = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", clean_text)
    #
    # Remove URLs and links
    clean_text = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([/a-z0-9\.-]*)*\/?', '', clean_text)
    clean_text = re.sub(r'([a-z0-9\.-]*)([/\\\*=]+)([a-z0-9\.-]*)', '', clean_text)

    #  Remove path-like phrases
    clean_text = re.sub(r'\/?([a-z0-9\.-_]*)\/([a-z0-9\.-_])*\/?', '', clean_text)

    return clean_text


def clean_emails(email_bodies):
    '''

    :param email_bodies:
    :return:
    '''
    # enron_emails['body'] = enron_emails['body'].map(lambda x: remove_html_markup(x))
    # enron_emails['body'] = enron_emails['body'].map(lambda x: clean_email(x))
    email_bodies = email_bodies.apply(remove_html_markup)
    email_bodies = email_bodies.apply(clean_email)
    return email_bodies

    # data['datetime'] = data['datetime'].apply(
    #     lambda x: dt.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ') if x != None else None)
