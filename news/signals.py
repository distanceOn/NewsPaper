from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group

@receiver(user_signed_up)
def add_user_to_common_group(sender, request, user, **kwargs):
    common_group, created = Group.objects.get_or_create(name='common')
    user.groups.add(common_group)