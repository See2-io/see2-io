# Django modules


# Third party modules
import os
import json
import pandas as pd
import numpy as np
from simpy.events import Event, NORMAL, Timeout

# See2-io modules
from sense.settings import ENRON_DATA_COLLECTION, ENRON_DATA_SIM
from sense.enron_emails.callbacks import process_email, user_signup


class EmailEvent(Event):
    """A :class:`~simpy.events.Event` that represents a sent email.

    This event is automatically triggered when it is created.

    """
    def __init__(self, env, delay=0, value=None):
        # if len(value) == 0:
        #     raise ValueError('No email_ids %s' % value)
        # NOTE: The following initialization code is inlined from
        # Event.__init__() for performance reasons.
        self.env = env
        self.callbacks = []
        self._value = value
        self._ok = True
        print('Event created at %d' % env.now)
        env.schedule(self, NORMAL, delay)

    def _desc(self):
        """Return a string *EmailEvent([value=value])*."""
        return '%s(%s)' % (self.__class__.__name__,
                             '' if self._value is None else
                             (', value=%s' % self._value))


def process_users(env):
    '''
    A processor to generate user sign-up events in simulation environment 'env'.
    :param env: an instance of :class: ~simpy.core.Environment, which controls the simulation.
    :return: Nothing
    '''
    fp = os.path.join(ENRON_DATA_SIM, 'enron_user_signups.json')
    with open(fp, 'r') as f:
        user_signups = json.load(f, )
        f.close()
    for user in user_signups:
        # print(user)
        delay = user['time'] - env.now
        event = Timeout(env, delay=delay, value=user)
        event.callbacks.append(user_signup)
        yield event


def send_emails(env):
    '''
    A processor to generate email events in simulation environment 'env'.
    :param env: an instance of :class: ~simpy.core.Environment, which controls the simulation.
    :return: Nothing
    '''
    fp = os.path.join(ENRON_DATA_COLLECTION, 'enron-emails.csv')
    enron_emails = pd.read_csv(fp,
                               # header=0,
                               # names=['id', ''cc', 'datetime', 'bcc', 'sender', 'recipients', 'subject', 'body',],
                               dtype={'id': np.int, 'cc': np.str, 'datetime': np.str, 'bcc': np.str, 'sender': np.str,
                                      'recipients': np.str, 'subject': np.str, 'body': np.str, },
                               parse_dates=[2]
                               )
    # Create row index from 'datetime' column
    enron_emails['datetime'] = pd.DatetimeIndex(enron_emails['datetime'].values)
    enron_emails = enron_emails.set_index('datetime', drop=False)
    enron_emails = enron_emails.sort_values(by='datetime')
    enron_emails = enron_emails.loc['1998-11-01':'2002-07-31']

    for index, row in enron_emails.iterrows():
        event = EmailEvent(env, delay=1, value=row)
        event.callbacks.append(process_email)
        val = yield event


def send_emails_by_freq(env, freq='D'):
    '''
    A processor to generate email events in simulation environment 'env'
    :param env: an instance of :class: ~simpy.core.Environment, which controls the simulation.
    :param freq: used in :method: ~pandas.DataFrame.groupby() to group emails by the given frequency
    :return: Nothing
    '''
    fp = os.path.join(ENRON_DATA_COLLECTION, 'enron-emails.csv')
    enron_emails = pd.read_csv(fp,
                               # header=0,
                               # names=['id', ''cc', 'datetime', 'bcc', 'sender', 'recipients', 'subject', 'body',],
                               dtype={'id': np.int, 'cc': np.str, 'datetime': np.str, 'bcc': np.str, 'sender': np.str,
                                      'recipients': np.str, 'subject': np.str, 'body': np.str, },
                               parse_dates=[2]
                               )
    # Create row index from 'datetime' column
    enron_emails['datetime'] = pd.DatetimeIndex(enron_emails['datetime'].values)
    enron_emails = enron_emails.set_index('datetime', drop=False)
    enron_emails = enron_emails.sort_values(by='datetime')
    enron_emails = enron_emails.loc['1998-11-01':'2002-07-31']
    print('Grouping by frequency "%s" ...' % freq)
    emails_by_freq = enron_emails.groupby(pd.Grouper(freq=freq))
    print('Processing emails ...')

    for name, group in emails_by_freq:
        print(name)
        event = EmailEvent(env, delay=1, value=group)
        event.callbacks.append(process_email)
        val = yield event
        # email_ids = []
        # for index, row in group.iterrows():
        #     email_ids.append(row.id)
        #     # TODO: remove work-around using delay=1 to prevent all events running at env.now(==0)
        #     e = EmailEvent(env, delay=1, value=row.id)
        #     # e = EmailEvent(env, delay=1, value=email_ids)
        #     e.callbacks.append(email_callback)
        #     # e.callbacks.append(register_user)
        #     val = yield e


def main():
    '''

    :return:
    '''
    process_users(None)


if __name__ == "__main__":
    main()
