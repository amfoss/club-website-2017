from django.db import models
from register.models import User_info

# Create your models here.
DOC_TYPE_CHOICE = (('sop','SoP'),('recomendation','Recomendation'),('resume','Resume'),('transcripts','Transcripts'),('other','Other'))

class Document(models.Model):
	doc_id = models.IntegerField( primary_key=True, blank=False, unique=True)
	username = models.ForeignKey(User_info, blank=False, null=False)
	d_type = models.CharField(max_length=15, choices=DOC_TYPE_CHOICE, blank=False, null=False)
	doc_file = models.FileField(upload_to='uploads/documents') 
	doc_timestamp = models.DateTimeField(auto_now_add=True)

