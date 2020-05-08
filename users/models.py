from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.contrib.auth.models import Permission

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=128, blank = True)
    last_name = models.CharField(max_length=128, blank = True)
    position = models.CharField(max_length=128, blank = True)
    contact_number = models.CharField(max_length=128, blank = True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])





@receiver(user_signed_up)
def after_user_signed_up(sender, request, user, **kwargs):
    # g = Group.objects.get(name='New User')
    viewCustomer = Permission.objects.get(name='Can view customer')
    addCustomer = Permission.objects.get(name='Can add customer')
    viewDistributor = Permission.objects.get(name='Can view distributor')
    addDistributor = Permission.objects.get(name='Can add distributor')
    viewProduct = Permission.objects.get(name='Can view product')
    addProduct = Permission.objects.get(name='Can add product')
    user.user_permissions.add(viewCustomer, addCustomer, viewDistributor, addDistributor, viewProduct, addProduct)
    # user.groups.add(g)
