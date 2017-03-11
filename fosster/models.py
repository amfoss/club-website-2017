from django.db import models


# Coming soon registration for email subscription
class Subscription(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
