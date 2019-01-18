# Add Django imports here
from django.contrib.auth.models import User

# Add third party imports here
import os
import json
import datetime
import pytz

# See2-io modules.
from sense.settings import ENRON_DATA_COLLECTION, ENRON_DATA_SIM, ENRON_SIM_PERIOD
from sense.enron_emails.data_filters import EmailAddressFilter
from sense.enron_emails.utils import FilteredDataSetsCache
from sense.enron_emails.vectorizer import top_topics
from sense.models import ADataFilter
from core.models import Person
from communities.models import Community, AMembership

# TODO: something better than these kludges to make the sim data available globally.
fp = os.path.join(ENRON_DATA_COLLECTION, 'edo_enron-custodians-data.json')
with open(fp) as f:
    user_data = json.load(f)
    f.close()
fp = os.path.join(ENRON_DATA_SIM, 'enron_sim_data.json')
with open(fp) as f:
    sim_data = json.load(f)
    f.close()
data_filters = FilteredDataSetsCache(name='Enron Corporation Emails')


def process_email(event):
    '''
    Process the email triggered by this event.
    :param event:  :class: ~sense.enron_emails.events.EmailEvent associated with this callback.
    :return: Nothing
    '''
    # The email from this event has been passed as the event.value
    email = event.value

    # For each data filter, if the sender is registered, add this email to its cache
    for data_filter in data_filters.get_data_filters():
        filter = data_filter.filter
        if email.sender[1:-1] in filter:
            # print(email.sender)
            data_filters.add_data(name=data_filter.name, data=email,)

    # Every ENRON_SIM_PERIOD, do something interesting with the cached datasets
    if event.env.now % ENRON_SIM_PERIOD == 0:
        # data_filters.process_caches(event.env.now)
        for key in data_filters.get_cache_keys():
            df = data_filters.get_filtered_data_cache(key)['Cache']
            if not df.empty:
                top_features = top_topics(df, 0.25, 0.02)
                print(top_features)
                timestamp = email.datetime.timestamp()
                data_filters.update_topics(timestamp=timestamp, name=key, new_topics=set(top_features),)


def user_signup(event):
    '''
    A call-back to deal with user sign-up events from the Enron sim.
    :param event: The event that triggered this call-back. It's value is the user's email address.
    :return: Nothing
    '''
    try:
        user_info = sim_data['Employees'][event.value['email']]
        user = User.objects.create(username=user_info['alternateName'],
                                   email=user_info['email'],
                                   password='password',)
        if 'affiliation' in user_info:
            if 'legalName' in user_info['affiliation']:
                user.user_profile.bio = '%s works for %s' % (user_info['name'], user_info['affiliation']['legalName'])
                user.user_profile.org = user_info['affiliation']['legalName']
        if 'jobTitle' in user_info:
            user.user_profile.job_title = user_info['jobTitle']

        # Add any community memberships
        if 'Communities' in user_info:
            for community in user_info['Communities']:
                if not community == 'Enron Corporation':
                    member, created = Person.objects.get_or_create(first_name=user_info['givenName'],
                                                              last_name=user_info['familyName'],
                                                              email=user_info['email'])
                    user.user_profile.member = member
                    community, created = Community.objects.get_or_create(name=community)
                    AMembership.objects.create(member=member,
                                               community=community,
                                               date_joined=datetime.datetime.now(pytz.utc),
                                               joining_reason='See2 rocks!',)
        user.user_profile.save()
        user.save()
        # print('User %s signed up at time %d after event ' % (event.value, event.env.now), event)
    except KeyError as e:
        pass
        # print('User %s not found in data' % event.value)

