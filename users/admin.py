from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.decorators import login_required

from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress, EmailConfirmation
from django.contrib.admin import AdminSite

from .forms import CustomUserCreationForm, CustomUserChangeForm
admin.site.login = login_required(admin.site.login)

CustomUser = get_user_model()

admin.site.unregister(Site)
admin.site.unregister(EmailAddress)
admin.site.unregister(EmailConfirmation)


class MyAdminSite(AdminSite):
    # Disable View on Site link on admin page
    site_url = None

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    site_url = None
    form = CustomUserChangeForm
    view_on_site = False
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name']


admin.site.register(CustomUser, CustomUserAdmin)
