from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import UserModel
import re

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('name', 'email', 'username', 'date_of_birth')

    def clean_password(self):
        passwd = len(self.cleaned_data['password'])
        if passwd and passwd < 8:
            raise ValidationError("Password must be greater than 8 characters")
        return str(self.cleaned_data['password'])

    def clean_name(self):
        if self.cleaned_data['name']:
            if not bool(re.match('^[a-zA-Z ]+$', self.cleaned_data['name'])):
                raise ValidationError("Name must only contain characters A to Z or a-z")
            else:
                return self.cleaned_data['name']
        return ""

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserModel
        fields = ('name', 'email', 'password', 'date_of_birth', 'is_active', 'is_admin', 'groups', 'user_permissions')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_admin',)
    filter_horizontal = ('groups',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('name', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Groups', {'fields': ('groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Register New User', {
            'classes': ('wide',),
            'fields': ('name', 'email', 'username', 'password', 'date_of_birth'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


# Now register the new UserAdmin...
admin.site.register(UserModel, UserAdmin)

