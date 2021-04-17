from django.contrib import admin
from myproject.custom_admin import custom_admin_site
from .models import TestModel

admin.site.register(TestModel)
custom_admin_site.register(TestModel)