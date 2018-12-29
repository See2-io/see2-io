# Add Django imports here

# Add third party imports here
import json

# Add local imports here


with open('./sense/enron_emails/data/in/edo_enron-custodians-data.json') as f:
    user_data = json.load(f)
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
    print('User %s signed up at time %d after event ' % (event.value, event.env.now), event)


def register_user(event):
    '''

    :param event: :class:simpy.events.Event associated with this callback.
    :return: Nothing
    '''
    print('-----------------%d----------------' % event.env.now)
    email = event.value
    # print(email)
    result = User.objects.filter(email=email['sender'][0])
    make_user(email['sender'][1:-1])
    # print(result)
    # group = event.value
    # for index, row in group.iterrows():
    #     print(row.sender)

    # UserManager().create_user(
    #     user['alternateName'],
    #     email=user['email'],
    #     first_name=user['givenName'],
    #     last_name=user['familyName'],
    # )

