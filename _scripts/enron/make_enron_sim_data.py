import os
from sense.settings import ENRON_DATA_COLLECTION, ENRON_DATA_SIM
import pandas as pd
import numpy as np
import json


def generate_user_signup_data():
    '''
    Make See2 signup times based simply on when the email address is first seen in the Enron emails.
    :return: Nothing
    '''
    fp = os.path.join(ENRON_DATA_COLLECTION, 'edo_enron-custodians-data.json')
    with open(fp) as f:
        user_data = json.load(f)
        f.close()

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
    # emails_by_day = enron_emails.groupby(pd.Grouper(freq='D')
    # for name, group in emails_by_day:

    user_signups = []
    for user in user_data:
        print('Looking for %s' % user['email'])
        for index, row in enron_emails.iterrows():
            if user['email'] == row.sender[1:-1]:
                print('Found in sender!')
                if row.id > 2:
                    user_signup = {'email': user['email'], 'time': row.id-2}
                else:
                    user_signup = {'email': user['email'], 'time': 0}
                user_signups.append(user_signup)
                break
            elif not pd.isnull(row.recipients):
                if user['email'] == row.recipients[1:-1]:
                    print('Found in recipients!')
                    if row.id > 2:
                        user_signup = {'email': user['email'], 'time': row.id - 2}
                    else:
                        user_signup = {'email': user['email'], 'time': 0}
                    user_signups.append(user_signup)
                    break
    user_signups_json = json.dumps(user_signups, indent=4)
    fp = os.path.join(ENRON_DATA_SIM, 'enron_user_signups.json')
    with open(fp, 'w') as f:
        f.write(user_signups_json)
        f.close()

    fp = os.path.join(ENRON_DATA_SIM, 'enron_user_signups.json')
    data = pd.read_json(fp)
    data.sort_values(by=['time'], inplace=True)
    data.to_json(path_or_buf=fp, orient='records')


def make_enron_sim_data():
    '''
    Script to generate a simulation file from the Enron data.
    :return: Nothing
    '''
    fp = os.path.join(ENRON_DATA_SIM, 'enron_user_signups.json')
    with open(fp) as f:
        enron_signups = json.load(f)
        f.close()
    fp = os.path.join(ENRON_DATA_COLLECTION, 'edo_enron-custodians-data.json')
    with open(fp) as f:
        enron_people = json.load(f)
        f.close()

    enron_sim_data = {}
    people = {}
    communities = {}
    communities['Presidents'] = {'Name': 'Presidents', 'Members': [],}
    communities['Traders'] = {'Name': 'Traders', 'Members': []}
    communities['Compliance'] = {'Name': 'Compliance', 'Members': [],}
    communities['Analysts'] = {'Name': 'Analysts', 'Members': [],}
    communities['Managers'] = {'Name': 'Managers', 'Members': [],}
    communities['Directors'] = {'Name': 'Directors', 'Members': [],}
    communities['CEOs'] = {'Name': 'CEOs', 'Members': []}

    for person in enron_people:
        # Add bio entries for each person
        people[person['email']] = person
        # Add people to their communities based on their job title
        if 'jobTitle' in person.keys():
            job = person['jobTitle'].lower()
            if 'president' in job:
                communities['Presidents']['Members'].append(person['email'])
            if ('trader' in job) or ('trading' in job):
                communities['Traders']['Members'].append(person['email'])
            if ('regulatory affairs' in job) or ('lawyer' in job) or ('risk' in job) or ('legal' in job) or ('counsel' in job) or ('admin' in job):
                communities['Compliance']['Members'].append(person['email'])
            if ('specialist' in job) or ('analys' in job):
                communities['Analysts']['Members'].append(person['email'])
            if ('manager' in job) or ('managing' in job):
                communities['Managers']['Members'].append(person['email'])
            if 'director' in job:
                communities['Directors']['Members'].append(person['email'])
            if ('ceo' in job) or ('chief' in job):
                communities['CEOs']['Members'].append(person['email'])

    for signup in enron_signups:
        # Add sim time step for See2 'signup' event scheduling.
        people[signup['email']]['see2_signup'] = signup['time']
        # Add this person's community memberships.
        people[signup['email']]['Communities'] = ['Enron Corporation']
        for key, community in communities.items():
            if signup['email'] in community['Members']:
                people[signup['email']]['Communities'].append(community['Name'])

    # Add people and communities to the sim data set.
    enron_sim_data['Employees'] = people
    enron_sim_data['Communities'] = communities

    fp = os.path.join(ENRON_DATA_SIM, 'enron_sim_data.json')
    with open(fp, 'w') as f:
        json.dump(enron_sim_data, f, indent=4)
        f.close()

    fp = os.path.join(ENRON_DATA_SIM, 'enron_user_signups.json')
    with open(fp, 'w') as f:
        json.dump(enron_signups, f, indent=4)
        f.close()


def main():
    '''
    main function to run scripts
    :return: Nothing
    '''
    # generate_user_signup_data()
    make_enron_sim_data()


if __name__ == "__main__":
    main()

