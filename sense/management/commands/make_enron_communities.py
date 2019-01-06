# Django modules.
from django.core.management.base import BaseCommand, CommandError

# Third party modules.
import json
import os

# See2-io modules.
from core.models import Person, Organisation, Bot
from communities.models import Community, AMembership, ACommunitySuperSub
from sense.models import DataSet, Custodian, FilteredDataSet, ADataFilter
from sense.settings import ENRON_DATA_COLLECTION, ENRON_DATA_SIM
from sense.enron_emails.data_filters import EmailAddressFilter


class Command(BaseCommand):
    help = 'Create the Enron super community and its sub-communities.'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('arg1', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            enron_community, created = Community.objects.get_or_create(name='Enron Corporation', super_community=True,)
            if created:
                # Create the 'God' dataset for use in the simulation.
                enron_god = Custodian.objects.create(actor=Organisation.objects.create(name='Enron Corporation',))
                enron_dataset = DataSet.objects.create(name='Enron Corporation Emails',
                                                       location=os.path.join('file:///', ENRON_DATA_COLLECTION, 'enron_emails.csv'),
                                                       custodian=enron_god,
                                                       )
                # Add all the members, i.e. the list of email addresses extracted from the Enron emails data set.
                fp = os.path.join(ENRON_DATA_COLLECTION, 'enron-distinct-users.json')
                with open(fp, 'r') as f:
                    items = json.load(f)
                    f.close()
                for item in items:
                    member = Person.objects.create(email=item)
                    membership = AMembership(member=member, community=enron_community, joining_reason='You know.')
                    membership.save()
                    print('Added member: %s to community %s.' % (membership.member.email, membership.community.name))
                items = []

                # Add the sub-communities based on known job titles
                # Note: members are only added during the simulation, when scheduled.
                fp = os.path.join(ENRON_DATA_SIM, 'enron_sim_data.json')
                with open(fp, 'r') as f:
                    items = json.load(f)
                    f.close()
                    #     for sub_community in items['Communities'].keys():
                    #         ACommunitySuperSub.objects.create(super_community=enron_community,
                    #                                           sub_community=Community.objects.create(name=sub_community))
                # Create the filtered community datasets in preparation for the enron simulation.
                for sub_community, members in items['Communities'].items():
                    custodian = Custodian.objects.create(actor=Organisation.objects.create(name='Enron %s' % sub_community,))
                    for k, v in members.items():
                        if k == 'Members':
                            filter = EmailAddressFilter(name=sub_community, filter=members['Members'])
                            location = os.path.join(ENRON_DATA_SIM, 'enron_'+sub_community.lower()+'_filtered_dataset.json')
                            filtered_dataset = FilteredDataSet.objects.create(name='Enron '+sub_community+' Filtered Dataset',
                                                                              location=location,
                                                                              custodian=custodian,
                                                                              )
                            data_filter = ADataFilter.objects.create(name='Enron '+sub_community+' Data Filter',
                                                                     dataset=enron_dataset,
                                                                     filtered_dataset=filtered_dataset,
                                                                     )
                            items = ''
                            for item in filter.filter:
                                items += item+','
                            data_filter.filter = items
                            data_filter.save()
            else:
                print('Enron super community already exists!')
        except Exception as err:
            raise CommandError('Unexpected error occurred: %s, type: %s' % (err, type(err)))
