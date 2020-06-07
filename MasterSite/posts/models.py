from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver


def upload_location(instance, filename):
    file_path = "posts/{creator_id}/{title}-{creationTime}-{filename}".format(creator_id=str(instance.creator.id), title=str(instance.title), creationTime=str(instance.creation_time), filename=filename)
    return file_path

class PostModel(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    update_time = models.DateTimeField(auto_now=True, verbose_name="date updated")
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    content = models.TextField(max_length=5000, null=False, blank=False)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=PostModel)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
