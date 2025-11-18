from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from quiz.models import Profile

# Create a profile when a new user is registered
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save profile whenever the user instance is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
