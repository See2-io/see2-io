# Add Django imports here
from django.core.management.base import BaseCommand, CommandError

# Add third party imports here
import json

# Add local imports here
from communities.models import Community, Member, AMembership, ACommunitySuperSub


class Command(BaseCommand):
    help = 'Create the Enron super community and its sub-communities.'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('arg1', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            c, created = Community.objects.get_or_create(name='Enron Corporation', super_community=True,)
            if created:
                # Add all the members, i.e. the list of email addresses extracted from the Enron emails data set.
                fp = './sense/enron_emails/data/in/enron-distinct-users.json'
                with open(fp, 'r') as f:
                    items = json.load(f)
                    f.close()
                for item in items:
                    m = Member.objects.create(email=item)
                    membership = AMembership(member=m, community=c, joining_reason='Stuff')
                    membership.save()
                    print('Added member: %s to community %s.' % (membership.member.email, membership.community.name))
                items = []

                # Add the sub-communities based on known job titles
                # Note: members are only added during the simulation, when scheduled.
                fp = './sense/enron_emails/data/in/enron_sim_data.json'
                with open(fp, 'r') as f:
                    items = json.load(f)
                    f.close()
                for community in items['Communities'].keys():
                    ACommunitySuperSub.objects.create(super_community=c,
                                                      sub_community=Community.objects.create(name=community))
            else:
                print('Enron super community already exists!')
        except Exception as err:
            raise CommandError('Unexpected error occurred: %s, type: %s' % (err, type(err)))
