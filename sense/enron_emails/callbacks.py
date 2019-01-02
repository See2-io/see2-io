# Add Django imports here
from django.contrib.auth.models import User

# Add third party imports here
import json
import datetime

# Add local imports here
from communities.models import Member, Community, AMembership

# TODO: something better than these kludges to make the sim data avilable globally.
with open('./sense/enron_emails/data/in/edo_enron-custodians-data.json') as f:
    user_data = json.load(f)
    f.close()
with open('./sense/enron_emails/data/in/enron_sim_data.json') as f:
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
                    m, created = Member.objects.get_or_create(first_name=user_info['givenName'],
                                                              last_name=user_info['familyName'],
                                                              email=user_info['email'])
                    user.user_profile.member = m
                    c, created = Community.objects.get_or_create(name=community)
                    AMembership.objects.create(member=m,
                                               community=c,
                                               date_joined=datetime.datetime.now(),
                                               joining_reason='See2 rocks!',)
        user.user_profile.save()
        user.save()
        print('User %s signed up at time %d after event ' % (event.value, event.env.now), event)
    except KeyError as e:
        print('User %s not found in data' % event.value)

