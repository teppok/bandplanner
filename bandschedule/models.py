from django.db import models

#from django.contrib.auth.models import User


class Calendar(models.Model):
    idstring = models.CharField(max_length=20)
    descstring = models.CharField(max_length=255)
    def __unicode__(self):
        return self.idstring.__str__()

    # get_calendar
    # Returns a Calendar object with the attached calendar_id string

    @classmethod
    def get_calendar(calendar_id):
        calendars = Calendar.objects.filter(idstring=calendar_id)
        
        if calendars.count() == 0:
            return None
    
        return calendars[0]

class SoftUser(models.Model):
    username = models.CharField(max_length=20)
    def __unicode__(self):
        return self.username.__str__()
    
    # create_softuser
    # When submitted an username, returns either an existing user object
    # with that username, or creates a new user and returns that object.
    # No password authentication is done.

    @classmethod
    def create_softuser(username):
        usertest = SoftUser.objects.filter(username=username)
        if usertest.count() == 0:
            user = SoftUser()
            user.username = username
            user.save()
            return user
        else:
            return usertest[0]
    


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

    # get_month_seen
    # Returns true if this month has been set as seen in calendar c by user u,
    # false otherwise.

    @classmethod
    def get_month_seen(this_date, c, user):
        if user is not None and this_date is not None and c is not None:
            month_seens = MonthSeen.objects.filter(month=this_date, user=user, calendar=c)
        
    #        print month_seens
            
            if month_seens.count() > 0:
                return True
            else:
                return False
        else:
            return False

