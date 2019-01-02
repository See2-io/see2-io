from django.db import models
from django.utils import timezone


class Community(models.Model):
    name = models.CharField('Community Name', max_length=128)
    super_community = models.BooleanField('Is a Super Community', default=False)
    inferred = models.BooleanField('Is inferred', default=False)
    members = models.ManyToManyField('Member', through='AMembership')
    sub_communities = models.ManyToManyField('self',
                                             through='ACommunitySuperSub',
                                             through_fields=('super_community', 'sub_community'),
                                             symmetrical=False)


class Member(models.Model):
    first_name = models.CharField('First Name', max_length=64, null=True, blank=True)
    last_name = models.CharField('Last Name', max_length=64,)
    email = models.EmailField('Email Address', null=True, blank=True)
    member_type = models.CharField('Membership Type', max_length=32, null=True, blank=True)


# TODO Remove work-around where 'CommunitySuperSub' and 'Membership' are prefixed with 'A' to ensure django migration in
# the necessary alphabetical order, i.e. classes with FKs are migrated before the classes they reference.
# Due to a 'bug' described at https://code.djangoproject.com/ticket/29182 and
# https://github.com/beda-software/drf-writable-nested/issues/64
class ACommunitySuperSub(models.Model):
    super_community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='super',)
    sub_community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='sub',)
    date_created = models.DateTimeField('Date sub-community joined', default=timezone.now,)


class AMembership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,)
    community = models.ForeignKey(Community, on_delete=models.CASCADE,)
    date_joined = models.DateTimeField('Date Joined', default=timezone.now,)
    joining_reason = models.CharField('Joining Reason', max_length=128, default='You know')

