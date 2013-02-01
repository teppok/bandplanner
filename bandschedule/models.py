from django.db import models
import random

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

    # approve_month
    # Based on the yesno parameter, either marks the month as seen
    # in the calendar object c by the user object user.
    
    def approve_month(self, user, this_date, yesno):
        
        month_seen = MonthSeen.objects.filter(month=this_date, user=user, calendar=self)
        
    #    print "Test months:", month_seen
        
        if yesno == "0":
            if month_seen.count() > 0:
                month_seen.delete()
    #            print "delete"
        else:
            if month_seen.count() == 0:
                newseen = MonthSeen()
                newseen.month = this_date
                newseen.user = user
                newseen.calendar = self
            
                newseen.save()
    #            print "New seen: ", newseen
                
        return

    # create_calendar
    # Creates a new calendar by the description string descstring. Forms a new
    # random ID string for the calendar and returns the generated object.

    @classmethod    
    def create_calendar(descstring):
        c = Calendar()
            
        c.idstring = ''.join(random.choice('0123456789') for x in range(20))
            
        c.descstring = descstring
        c.save()
    
        return c
    
    
    # toggle_date
    # Toggles the availability for date object requestdate in calendar object c for user object 'user'.
    
    def toggle_date(self, user, requestdate):
        d = DateInfo.objects.filter(date=requestdate, user=user, calendar=self)
        
    #        print "Calendar objects: ", c
    
    #        print d.count()
        
        if d.count() > 0:
            d.delete()
    #            print DateInfo.objects.all()
        else:
            d = DateInfo()
            d.date = requestdate
            d.dateok = False
            d.calendar = self
            d.user = user
    #            print "Constructed d: ", d
            d.save()
    


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

