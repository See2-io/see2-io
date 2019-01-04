from sense.settings import ENRON_DATA_COLLECTION
import os
import json


def enrich_user_data():
    '''

    :return:
    '''
    fp = os.path.join(ENRON_DATA_COLLECTION, 'enron-distinct-users.json')
    with open(fp) as f:
        user_emails = json.load(f)
        f.close()
    fp = os.path.join(ENRON_DATA_COLLECTION, 'edo_enron-custodians-data.json')
    with open(fp) as f:
        user_data = json.load(f)
        f.close()
    count = 0
    for user in user_data:
        # print(user)
        # print(user['email'])
        if user['email'] in user_emails:
            count += 1
            print(count)


def main():
    '''

    :return:
    '''
    enrich_user_data()


if __name__ == "__main__":
    main()
