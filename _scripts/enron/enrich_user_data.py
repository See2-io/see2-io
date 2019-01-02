import os
import json


def enrich_user_data():
    '''

    :return:
    '''
    print(os.getcwd())

    with open('../../data/in/enron-distinct-users.json') as f:
        user_emails = json.load(f)
        f.close()
    with open('../../data/in/edo_enron-custodians-data.json') as f:
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
