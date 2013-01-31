# coding=UTF-8
# Create your views here.

from django.http import HttpResponse
from models import Calendar, DateInfo, SoftUser, MonthSeen
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.utils import simplejson
import random
import datetime

def index(request):
    return HttpResponse("Yo")

def new_calendar(request):
    context = {}
    return render(request, 'bandschedule/new_calendar.html', context)

def get_calendar(calendar_id):
    calendars = Calendar.objects.filter(idstring=calendar_id)
    
    if calendars.count() == 0:
        return None

    return calendars[0]
    

def monthly_view(request, calendar_id, year=None, month=None):
    
    if 'user' in request.session:
        username = request.session['user']
    else:
        username = None

    (month_table, year, month, c, user) = get_month_with_blind_data(year, month, calendar_id, username)

    if month_table == None:
        return
    
    if month == 12:
        next_month = str(year+1) + "/1/"
    else:
        next_month = str(year) + "/" + str(month+1) + "/"

    if month == 1:
        prev_month = str(year-1) + "/12/"
    else:
        prev_month = str(year) + "/" + str(month-1) + "/"
    
#    if username is None:
#        username = ""
    this_date = datetime.date(year,month,1)
    month_seen = get_month_seen(this_date, c, user)
        
    month_seen_by = create_month_seen_by(this_date, c)

    if username == None:
        username = ""

    context = { 'calendar_id' : calendar_id, 'month_table' : month_table,
               'next_month': next_month, 'prev_month' : prev_month,
               'year': year, 'month': month, 'user': username,
               'month_seen': month_seen, 'month_seen_by': month_seen_by,
               'descstring': c.descstring }
    
    return render(request, 'bandschedule/monthly.html', context)

def get_month_seen(this_date, c, user):
    if user is not None:
        month_seens = MonthSeen.objects.filter(month=this_date, user=user, calendar=c)
    
#        print month_seens
        
        if month_seens.count() > 0:
            return True
        else:
            return False
    else:
        return False
    

def create_softuser(username):
    usertest = SoftUser.objects.filter(username=username)
    if usertest.count() == 0:
        user = SoftUser()
        user.username = username
        user.save()
        return user
    else:
        return usertest[0]

    
        

def login_user(request):
    params = request.GET
    if 'user' not in params:
        return HttpResponse("")
#    print "Login", params['user']
    
    request.session['user'] = params['user']
    return HttpResponse("Ok")

def logout_user(request):
    if 'user' not in request.session:
        return HttpResponse("")

    del request.session['user']
    return HttpResponse("Ok")

def get_month(request):
    params = request.GET
#    print params
    if 'calendar_id' not in params or \
        'year' not in params or \
        'month' not in params:
        return HttpResponse("")
    
    calendar_id = params['calendar_id']
    year = params['year']
    month = params['month']

    if 'user' in request.session:
        username = request.session['user']
    else:
        username = None
#    print "aaa"
    (month_table, year, month, c, user) = get_month_with_blind_data(year, month, calendar_id, username)

    this_date = datetime.date(year,month,1)
    month_seen = get_month_seen(this_date, c, user)

    simple_data = { 'month' : month_table, 'month_seen' : month_seen }
#    print simplejson.dumps(simple_data)
    return HttpResponse(simplejson.dumps(simple_data), mimetype="application/json")

def get_month_with_blind_data(year, month, calendar_id, username):
    c = get_calendar(calendar_id)
    if (c == None):
        return None

    if username == None:
        user = None
    else:
        user = create_softuser(username)
    
    currDate = datetime.date.today()

    if year is None:
        year = currDate.year
    else:
        year = int(year)
        
    if month is None:
        month = currDate.month
    else:
        month = int(month)
        
    return (create_month(year, month, c, user), year, month, c, user)

def create_month_seen_by(this_date, calendar):
    users = SoftUser.objects.filter(monthseen__month__exact=this_date, monthseen__calendar=calendar)
#    print users
    if users.count() == 0:
        return "(No one yet)"
    result_string = "<ul>"
    for user in users:
        result_string = result_string + "<li>" + user.username + "</li>"
    
    result_string = result_string + "</ul>"

    return result_string
    
def approve_month_request(request):
    params = request.GET
#    print params
    if request.method == 'GET':
        if 'year' not in params or \
           'month' not in params or \
           'calendar_id' not in params or \
           'yesno' not in params or \
           'user' not in request.session:
            return HttpResponse("")
        
        year = int(params['year'])
        month = int(params['month'])
        username = request.session['user']
        calendar_id = params['calendar_id']
        yesno = params['yesno']

        approve_table = approve_month(year, month, calendar_id, username, yesno)
        
        simple_data = { 'month_seen_by' : approve_table }
        
        return HttpResponse(simplejson.dumps(simple_data), mimetype="application/json")

    
def approve_month(year, month, calendar_id, username, yesno):
    user = create_softuser(username)
    this_date = datetime.date(year,month,1)
    
    c = get_calendar(calendar_id)
    if (c == None):
        return
    
    month_seen = MonthSeen.objects.filter(month=this_date, user__username=username, calendar=c)
    
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
            newseen.calendar = c
        
            newseen.save()
#            print "New seen: ", newseen
            
    return create_month_seen_by(this_date, c)
    

def create_calendar(request):
    params = request.POST

    if request.method == 'POST' and 'descstring' in params:
        c = Calendar()
        
        c.idstring = ''.join(random.choice('0123456789') for x in range(20))
        
        c.descstring = params['descstring']
#        print c.idstring
#        print c.descstring
        c.save()
        
        return redirect('monthly_view', calendar_id=c.idstring)
    else:
        return HttpResponse("Failed")
        

def create_row(thisDate, calendar, user):
    calendarString = ""
    
    subDate = datetime.timedelta(days=thisDate.weekday())
    modDate = thisDate - subDate
    
    for i in range(0, 7):
        d = DateInfo.objects.filter(date=modDate, calendar=calendar)
        d2 = d.filter(user=user)
        idstring = str(modDate.year)+"-"+str(modDate.month)+"-"+str(modDate.day)
#        calendarString = calendarString + "<td>"
        if d.count() == 0:
            calendarString = calendarString + "<td id='" + idstring + "' class='tablecell green'>"
        elif d2.count() == 0:
            calendarString = calendarString + "<td id='" + idstring + "' class='tablecell yellow'>"
        else:
            calendarString = calendarString + "<td id='" + idstring + "' class='tablecell red'>"
        
        if user is not None:
            calendarString = calendarString + "<a href='#' onclick='toggle(" + \
                str(modDate.year) + "," + str(modDate.month) + "," + str(modDate.day) +");'>"
        
        calendarString = calendarString + str(modDate.day) + "." + str(modDate.month)
        if user is not None:
            calendarString = calendarString + "</a>"
        calendarString = calendarString + "</td>"
        modDate = modDate + datetime.timedelta(days=1)
        
    return (calendarString, modDate)

def create_month(year, month, calendar, user):
    thisDate = datetime.date(year,month,1)
    calendarString = "<table>"
    count = 0
    
    while (thisDate.month <= month and thisDate.year <= year) and count < 7:
        calendarString = calendarString + "<tr>"
        (newRow, newDate) = create_row(thisDate, calendar, user)
        calendarString = calendarString + newRow
        count = count + 1

        thisDate = newDate
        calendarString = calendarString + "</tr>"
        
    return calendarString + "</table>"

    

def toggle_date(request):
    params = request.GET
    if request.method == 'GET':
        if 'year' not in params or \
           'month' not in params or \
           'targetyear' not in params or \
           'targetmonth' not in params or \
           'targetday' not in params or \
           'calendar_id' not in params or \
           'user' not in request.session:
            return HttpResponse("")
        
        year = int(params['year'])
        month = int(params['month'])
        targetyear = int(params['targetyear'])
        targetmonth = int(params['targetmonth'])
        targetday = int(params['targetday'])
        username = request.session['user']
        calendar_id = params['calendar_id']
        
        requestdate = datetime.date(targetyear, targetmonth, targetday)
#        print requestdate

        user = create_softuser(username)
        
        c = get_calendar(calendar_id)
        if (c == None):
            return

        d = DateInfo.objects.filter(date=requestdate, user=user, calendar=c)
        
#        print "Calendar objects: ", c

#        print d.count()
        
        if d.count() > 0:
            d.delete()
#            print DateInfo.objects.all()
        else:
            d = DateInfo()
            d.date = requestdate
            d.dateok = False
            d.calendar = c
            d.user = user
#            print "Constructed d: ", d
            d.save()

            
        (month_table, year, month, c, user) = get_month_with_blind_data(year, month, calendar_id, username)

        simple_data = { 'month' : month_table }
        
        return HttpResponse(simplejson.dumps(simple_data), mimetype="application/json")
            
