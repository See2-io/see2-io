# Add Django imports here
from django.contrib.auth.models import User

# Add third party imports here
import os
import json
import datetime

# See2-io modules.
from sense.settings import ENRON_DATA_COLLECTION, ENRON_DATA_SIM
from core.models import Person
from communities.models import Community, AMembership

# TODO: something better than these kludges to make the sim data avilable globally.
fp = os.path.join(ENRON_DATA_COLLECTION, 'edo_enron-custodians-data.json')
with open(fp) as f:
    user_data = json.load(f)
    f.close()
fp = os.path.join(ENRON_DATA_SIM, 'enron_sim_data.json')
with open(fp) as f:
    sim_data = json.load(f)
    f.close()


def process_email(event):
    '''
    Process the email triggered by this event.
    :param event:  :class: ~sense.enron_emails.events.EmailEvent associated with this callback.
    :return: Nothing
    '''
    email = event.value
    # print(email)


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
                                               date_joined=datetime.datetime.now(),
                                               joining_reason='See2 rocks!',)
        user.user_profile.save()
        user.save()
        print('User %s signed up at time %d after event ' % (event.value, event.env.now), event)
    except KeyError as e:
        print('User %s not found in data' % event.value)

