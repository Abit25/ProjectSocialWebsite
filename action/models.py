from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

# Create your models here.
class Action(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    verb=models.CharField(max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    target_ct=models.ForeignKey(ContentType,on_delete=models.CASCADE,related_name='target_object',blank=True,null=True)
    target_id=models.PositiveIntegerField(null=True,blank=True,db_index=True)
    target=GenericForeignKey('target_ct','target_id')
