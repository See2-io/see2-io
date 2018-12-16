from django.contrib import admin

# Register your models here.
from .models import Community, Member

admin.site.register(Community)
admin.site.register(Member)
