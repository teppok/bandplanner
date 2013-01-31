"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from models import Calendar, MonthSeen, SoftUser
from django.test import TestCase
from views import create_calendar, toggle_date, create_month, approve_month, approve_month_request, create_softuser
from django.http import HttpRequest

#client = Client()

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class CalendarTest(TestCase):
    def test_calendar(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST = { 'descstring': 'testi' }
        create_calendar(request)
        
    def testDate(self):
        self.test_calendar()
        c = Calendar.objects.all()
#        self.assertEqual(c.count(), 1)
        
        calendar_id = c[0].idstring
        print "Calendar id: ", calendar_id
        
        dateinfo = self.client.get("/schedule/toggle", {'year':2012, 'month':12, 'day':22, 'calendar': calendar_id })
#        request = HttpRequest()
#        request.method = 'GET'
#        request.GET = {'year':2012, 'month':12, 'day':22, 'calendar': calendar_id }
#        request.session['user'] = 'test'
#        dateinfo = toggle_date(request)
        print "Returned dateinfo: ", dateinfo
#        dateinfo = toggle_date(request)
        dateinfo = self.client.get("/schedule/toggle", {'year':2012, 'month':12, 'day':22, 'calendar': calendar_id })
        print "Returned dateinfo 2: ", dateinfo
        
    def test_create_calendar(self):
        #print create_month(2012,12)
        pass

#    def login_user(self, username):
#        request = HttpRequest()
#        request.method = 'GET'
#        request.GET = {'year':2012, 'month':12, 'calendar': calendar_id, 'user':'test' }
        
        
    def test_month_seen(self):
        print "Month_seen test"
        self.test_calendar()
        c = Calendar.objects.all()
        calendar_id = c[0].idstring
        print "Calendar id: ", calendar_id
        user = create_softuser('test2')
        
        print SoftUser.objects.all()
        print Calendar.objects.all()
        print MonthSeen.objects.all()
        approve_month(2012, 12, calendar_id, user, 1)
        print SoftUser.objects.all()
        print Calendar.objects.all()
        print MonthSeen.objects.all()
        approve_month(2013, 1, calendar_id, user, 1)
        print SoftUser.objects.all()
        print Calendar.objects.all()
        print MonthSeen.objects.all()
        approve_month(2013, 1, calendar_id, user, 0)
        print SoftUser.objects.all()
        print Calendar.objects.all()
        print MonthSeen.objects.all()
#        request = HttpRequest()
#        request.method = 'GET'
#        request.GET = {'year':2012, 'month':12, 'calendar': calendar_id, 'user':'test' }
#        request.session['user'] = 'test'
#        print month_seen(request)
    