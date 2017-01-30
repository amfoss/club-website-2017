import os

# Django Libraries
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
from register.models import User_info


FOLDER_CHOICE = (
    ('technical', 'Technical'), ('fun', 'Fun'), ('other', 'Other'))


"""
Function to get dynamic image path. 
It creates folder if it does not exist.
"""

def content_file_name(instance, filename):
    upload_dir = os.path.join('images/uploads', \
        instance.folder_name.folder_name)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)


"""
Model to store the folder details; 
'technical' or 'fun' or 'others' category
"""

class Folder(models.Model):
    folder_name = models.CharField(max_length=50,  unique=True,\
         primary_key=True, blank=False, null=False)
    folder_description = models.CharField(max_length=200)
    folder_type = models.CharField(max_length=15, \
        choices=FOLDER_CHOICE, blank=False, null=False)


"""
Model to store images corresponding to the folder.
"""
class Image(models.Model):
    img = models.ImageField(upload_to=content_file_name )
    folder_name = models.ForeignKey(Folder, blank=False, null=False)

    class Meta:
        unique_together = ('img','folder_name')


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to. This file storage 
        solves overwrite on upload problem.
        """
        if self.exists(name):
            os.remove(os.path.join("", name))
        return name




class ProfileImage(models.Model):
    """
    Model to store profile images of users.
    One to one relation with User_info model.
    """
    image = models.ImageField(upload_to="images/profile_image/", \
            storage=OverwriteStorage(), blank=False, null=False)
    username = models.ForeignKey(User_info, blank=False, null=False)


@receiver(models.signals.post_delete, sender=ProfileImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)