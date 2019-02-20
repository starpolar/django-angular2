from django.db import models


class PubUser(models.Model):
    user_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')



