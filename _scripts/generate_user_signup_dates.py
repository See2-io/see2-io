import pandas as pd
import numpy as np
import json
import math


def generate_user_signup_data():
    '''

    :return:
    '''
    # with open('../sense/enron_emails/data/in/edo_enron-custodians-data.json') as f:
    #     user_data = json.load(f)
    #     f.close()
    #
    # enron_emails = pd.read_csv('../sense/enron_emails/data/in/enron-emails.csv',
    #                            # header=0,
    #                            # names=['id', ''cc', 'datetime', 'bcc', 'sender', 'recipients', 'subject', 'body',],
    #                            dtype={'id': np.int, 'cc': np.str, 'datetime': np.str, 'bcc': np.str, 'sender': np.str,
    #                                   'recipients': np.str, 'subject': np.str, 'body': np.str, },
    #                            parse_dates=[2]
    #                            )
    # # Create row index from 'datetime' column
    # enron_emails['datetime'] = pd.DatetimeIndex(enron_emails['datetime'].values)
    # enron_emails = enron_emails.set_index('datetime', drop=False)
    # enron_emails = enron_emails.sort_values(by='datetime')
    # enron_emails = enron_emails.loc['1998-11-01':'2002-07-31']
    # # emails_by_day = enron_emails.groupby(pd.Grouper(freq='D')
    # # for name, group in emails_by_day:
    #
    # user_signups = []
    # for user in user_data:
    #     print('Looking for %s' % user['email'])
    #     for index, row in enron_emails.iterrows():
    #         if user['email'] == row.sender[1:-1]:
    #             print('Found in sender!')
    #             if row.id > 2:
    #                 user_signup = {'email': user['email'], 'time': row.id-2}
    #             else:
    #                 user_signup = {'email': user['email'], 'time': 0}
    #             user_signups.append(user_signup)
    #             break
    #         elif not pd.isnull(row.recipients):
    #             if user['email'] == row.recipients[1:-1]:
    #                 print('Found in recipients!')
    #                 if row.id > 2:
    #                     user_signup = {'email': user['email'], 'time': row.id - 2}
    #                 else:
    #                     user_signup = {'email': user['email'], 'time': 0}
    #                 user_signups.append(user_signup)
    #                 break
    # user_signups_json = json.dumps(user_signups, indent=4)
    # file_path = '../sense/enron_emails/data/in/enron_user_signups.json'
    # with open(file_path, 'w') as f:
    #     f.write(user_signups_json)
    #     f.close()

    data = pd.read_json('../sense/enron_emails/data/in/enron_user_signups.json')
    data.sort_values(by=['time'], inplace=True)
    data.to_json(path_or_buf='../sense/enron_emails/data/in/enron_user_signups.json', orient='records')


def main():
    '''

    :return:
    '''
    generate_user_signup_data()


if __name__ == "__main__":
    main()
