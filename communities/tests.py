from django.test import TestCase
import datetime
from django.utils import timezone

from .models import Community


class CommunityModelTests(TestCase):

    def test_not_sub_community_of_self(self):
        """
        add_sub_community does not allow 'self' community to be added as a sub-community.
        """
        super_community = Community.objects.create(name='Super Community', super_community=True,)
        community = Community.objects.create(name='Community')

        self.assertIs(super_community.super_community, True)
        self.assertIs(community.super_community, False)

