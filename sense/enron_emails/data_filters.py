# Third party modules:


# See2-io modules.

class EmailAddressFilter:
    '''
    A class to filter (Enron) email data by email address
    :attr name: The name of a filter instance.
    :attr filter: The filter to be applied to the incoming data. In this case a list of email addresses
    '''

    def __init__(self, name, filter):
        self.name = name
        self.filter = filter

    def filter(self, data):
        '''

        :param data: the data to be filtered
        :return: filtered data
        '''
        return data
