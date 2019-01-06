# Django modules
from django.contrib import admin

# See2-io modules
from .models import DataSet, FilteredDataSet, Custodian, PublishedDataSet, DataSetContract, DataLicence

admin.site.register(DataSet)
admin.site.register(FilteredDataSet)
admin.site.register(Custodian)
admin.site.register(PublishedDataSet)
admin.site.register(DataSetContract)
admin.site.register(DataLicence)
