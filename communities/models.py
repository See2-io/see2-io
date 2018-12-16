from django.db import models
from django.utils import timezone

# Create your models here.


class Community(models.Model):
    name = models.CharField('Community Name', max_length=128,)
    super_community = models.BooleanField('Is a Super Community', default=False,)
    inferred = models.BooleanField('Is inferred', default=False,)
    members = models.ManyToManyField('Member', through='Membership',)
    sub_communities = models.ManyToManyField('Community', through='CommunityParentChild',)


class Member(models.Model):
    first_name = models.CharField('First Name', max_length=64,)
    middle_names = models.CharField('Middle Names', max_length=64,)
    last_name = models.CharField('Last Name', max_length=64,)
    member_type = models.CharField('Membership Type', max_length=32,)


class CommunityParentChild(models.Model):
    parent = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='parent',)
    child = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='child',)
    date_created = models.DateTimeField('Date sub-community joined', default=timezone.now,)


class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,)
    community = models.ForeignKey(Community, on_delete=models.CASCADE,)
    date_joined = models.DateTimeField('Date Joined', default=timezone.now,)
    joining_reason = models.CharField('Joining Reason', max_length=128,)

