from django.contrib import admin

# Register your models here.
from .models import Studies, Profile

admin.site.register(Studies)
admin.site.register(Profile)