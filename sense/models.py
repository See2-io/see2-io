# Django modules.
from django.db import models

# See2-io modules
from core.models import Actor

# Sense models
# TODO: Remove work-around when bug fixed.
# Some classes maybe prefixed with 'A' to ensure they preceed other classes alphabetically. This is to work-around
# a bug involving FKs where the class declaring the FK must be migrated _before_ the class referred to by the FK.
# See 'bug' described at https://code.djangoproject.com/ticket/29182 and
# https://github.com/beda-software/drf-writable-nested/issues/64


# class CommaSepField(models.Field):
#     "Implements comma-separated storage of lists"
#
#     def __init__(self, separator=",", *args, **kwargs):
#         self.separator = separator
#         super().__init__(*args, **kwargs)
#
#     def deconstruct(self):
#         name, path, args, kwargs = super().deconstruct()
#         # Only include kwarg if it's not the default
#         if self.separator != ",":
#             kwargs['separator'] = self.separator
#         return name, path, args, kwargs


class DataSet(models.Model):
    '''
    A DataSet can represent any collection of data, structured or not, in any form of media.
    '''
    name = models.CharField(max_length=32, default='Please name me!',)
    location = models.URLField()
    custodian = models.ForeignKey('Custodian', on_delete=models.CASCADE)


class Custodian(models.Model):
    '''
    Proxy class for an actor in the See2 ecosystem.
    '''
    actor = models.OneToOneField(Actor, on_delete=models.CASCADE)


class FilteredDataSet(models.Model):
    '''
    A FilteredDataSet is a subset of a DataSet resulting from the application of a filter.
    The Custodian is implicitly the same as the source DataSet(s), i.e. only a Custodian can produce a filtered data
    set.
    '''
    name = models.CharField(max_length=32, default='Please name me!',)
    location = models.URLField()
    data_sets = models.ManyToManyField('DataSet', through='ADataFilter',)
    custodian = models.ForeignKey('Custodian', on_delete=models.CASCADE,)


class ADataFilter(models.Model):
    '''
    A DataFilter is applied to one or more DataSets to produce some subset of the source data set(s).
    '''
    name = models.CharField(max_length=32)
    dataset = models.ForeignKey('DataSet', on_delete=models.CASCADE,)
    filtered_dataset = models.ForeignKey('FilteredDataSet', on_delete=models.CASCADE,)
    date_applied = models.DateTimeField(auto_now=True,)
    filter = models.CharField(max_length=2048,)


class PublishedDataSet(models.Model):
    '''

    '''
    name = models.CharField(max_length=32,)
    filtered_datasets = models.ManyToManyField('FilteredDataSet', through='APublication',)
    contract = models.ForeignKey('DataSetContract', on_delete=models.CASCADE, null=True,)
    licence = models.ForeignKey('DataLicence', on_delete=models.CASCADE, null=True,)


class APublication(models.Model):
    filtered_dataset = models.ForeignKey('FilteredDataSet', on_delete=models.CASCADE,)
    published_dataset = models.ForeignKey('PublishedDataSet', on_delete=models.CASCADE,)
    publication_date = models.DateTimeField(auto_now=True,)


class DataSetContract(models.Model):
    '''

    '''
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256,)
    url = models.URLField()
    parties = models.ManyToManyField(Actor, through='AContractParty')


class AContractParty(models.Model):
    '''

    '''
    party = models.ForeignKey(Actor, on_delete=models.CASCADE,)
    contract = models.ForeignKey('DataSetContract', on_delete=models.CASCADE,)
    contract_date = models.DateTimeField(auto_now=True,)


class DataLicence(models.Model):
    '''

    '''
    name = models.CharField(max_length=32,)
    description = models.CharField(max_length=256,)
    url = models.URLField()
