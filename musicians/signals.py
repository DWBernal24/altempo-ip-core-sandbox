from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from musicians.models import Feedback

@receiver([post_save, post_delete], sender=Feedback)
def update_musician_score_on_feedback_change(sender, instance, **kwargs):
    instance.music_project.update_score()
