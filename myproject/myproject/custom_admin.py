from django.contrib import admin
from myapp.models import TestModel
from user_registration.models import UserModel

class MyCustomAdmin(admin.AdminSite):
    site_header = "My Custom Admin"
    site_title = "Custom Admin"
    index_title = "Welcom to custom admin"

custom_admin_site = MyCustomAdmin(name='custom_admin_site')