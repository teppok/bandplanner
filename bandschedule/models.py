from django.db import models

#from django.contrib.auth.models import User


class Calendar(models.Model):
    idstring = models.CharField(max_length=20)
    descstring = models.CharField(max_length=255)
    def __unicode__(self):
        return self.idstring.__str__()

class SoftUser(models.Model):
    username = models.CharField(max_length=20)
    def __unicode__(self):
        return self.username.__str__()

# Create your models here.
class DateInfo(models.Model):
    dateok = models.BooleanField()
    date = models.DateField()
    calendar = models.ForeignKey(Calendar)
    user = models.ForeignKey(SoftUser)
    def __unicode__(self):
        return self.date.__str__()
    
class MonthSeen(models.Model):
    user = models.ForeignKey(SoftUser)
    calendar = models.ForeignKey(Calendar)
    # month = datefield that contains the 1st day of a month.
    month = models.DateField()
    def __unicode__(self):
        return self.month.__str__()
#        return self.user.__str__() + ": " + self.month.__str__() + " in " + self.calendar.__str__()
        
