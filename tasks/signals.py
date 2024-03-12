from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


# @receiver(post_save, sender=Payment)
# def increment_agent_referral_count(sender, instance, created, **kwargs):
#     print("in here............")
#     if created:
#         agent = instance.booking.agent
#         seats = BookingSeat.objects.filter(booking=instance.booking).count()
#         if agent:
#             AgentReferral.objects.create(
#                 agent=agent, no_of_passengers=seats, initiated_by=instance.initiator
#             )
