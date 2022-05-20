from django.contrib import admin
from .models import Location, Chore, Profile, List

admin.site.register(Location)
admin.site.register(Chore)
admin.site.register(Profile)
admin.site.register(List)