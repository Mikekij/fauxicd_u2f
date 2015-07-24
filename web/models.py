from django.db import models

# Create your models here.

class Icd(models.Model):
    name = models.CharField(max_length=128, unique=True)
    zap_duration = models.IntegerField(default=0) #duration of a zap in milliseconds
    keys_required = models.IntegerField(default=2) #num of encryption keys required to execute

#    def save(self, *args, **kwargs):
#        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
