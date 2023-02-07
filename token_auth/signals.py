from django.dispatch import receiver
from django.db.models import signals
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_user_token_after_registration(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


post_save.connect(create_user_token_after_registration, sender=User)
