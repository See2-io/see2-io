# Django modules
from django.contrib import admin

# See2-io modules
from .models import Actor, Person, Organisation, Bot

admin.site.register(Actor)
admin.site.register(Person)
admin.site.register(Organisation)
admin.site.register(Bot)
