# Django libraries
from django.forms import ModelForm
from django import forms


# Application specific imports
from images.models import Folder

class FolderForm(ModelForm):
    """
    folder_name=forms.CharField(
         required=True,
         label='folder_name',
         widget=forms.TextInput(
            attrs={'placeholder': 'Event Name'}
         )
    )

    folder_description=forms.CharField(
         required=True,
         label='folder_description',
         widget=forms.Textarea(
            attrs={'placeholder': 'Description of Event', \
            'cols': 20, 'rows': 5}
         )
    )
    """
    class Meta:
        model = Folder
