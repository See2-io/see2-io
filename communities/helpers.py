# Django modules
from django.contrib.auth.models import User, UserManager

# Third party modules


# Local modules
from communities.models import Community, Member


def add_member(user, community):
    '''
    Add :param: user as a member of :class: ~communities.models.Community community.
    :param user:  a python dictionary containing user attributes.
    :param community: a :class: ~communities.models.Community object.
    :return:
    '''
    community.members