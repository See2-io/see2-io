# Add Django imports here
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# Add third party imports here

# Add local imports here
from communities.models import Community


class Command(BaseCommand):
    help = 'Runs the specified simulation.'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('arg1', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            self.delete_enron_community()
        except Exception as err:
            raise CommandError('Unexpected error occurred: %s, type: %s' % (err, type(err)))

    def delete_enron_community(self):
        '''

        :return:
        '''
        try:
            # Retrieve the 'Enron Corporation' object.
            community = Community.objects.get(name='Enron Corporation',)
            # Delete all the members
            community.members.all().delete()
            # Delete any sub-communities
            for sub_community in community.sub_communities.all():
                sub_community.members.all().delete()
                sub_community.delete()
            community.delete()
            # Delete See2 users associated with Enron Corporation
            User.objects.all().delete()
            # User.objects.all().filter(user_profile.org='Enron Corporation').delete()
        except ObjectDoesNotExist:
            print("The 'Enron Corporation' Community doesn't exist!")
        except Exception as err:
            raise CommandError('Unexpected error occurred: %s, type: %s' % (err, type(err)))
