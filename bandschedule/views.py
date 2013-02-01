# coding=UTF-8
# Create your views here.

from django.http import HttpResponse
from models import Calendar, DateInfo, SoftUser, MonthSeen
from django.shortcuts import render, redirect
from django.template import Context, Template
from django.utils import simplejson
import random
import datetime

# ------- INITIALIZATION -------------

# append_data
# Gets the Calendar object with the supplied calendar_id.
# If username string exists, gets the user object having that name.
# If year or month are None, looks at the current date to fetch year and month.
# Returns the found objects.

def append_data(year, month, calendar_id, username):
    c = Calendar.get_calendar(calendar_id)
    if (c == None):
        return None

    if username == None:
        user = None
    else:
        user = SoftUser.create_softuser(username)
    
    currDate = datetime.date.today()

    if year is None:
        year = currDate.year
    else:
        year = int(year)
        
    if month is None:
        month = currDate.month
    else:
        month = int(month)
        
    return (year, month, c, user)

# ------- CONTROLLERS ----------

# approve_month
# Based on the yesno parameter, either marks the month as seen
# in the calendar object c by the user object user.
    
def approve_month(c, user, this_date, yesno):
    
    month_seen = MonthSeen.objects.filter(month=this_date, user=user, calendar=c)
    
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
            
    return


# create_calendar
# Creates a new calendar by the description string descstring. Forms a new
# random ID string for the calendar and returns the generated object.

def create_calendar(descstring):
    c = Calendar()
        
    c.idstring = ''.join(random.choice('0123456789') for x in range(20))
        
    c.descstring = descstring
    c.save()

    return c


# toggle_date
# Toggles the availability for date object requestdate in calendar object c for user object 'user'.

def toggle_date(c, user, requestdate):
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




# ------- HTML CREATION ----------

# create_month_seen_by
# Creates a HTML list containing the users that have seen the 
# supplied month object at date supplied by the date object this_date

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



# create_month_table
# Creates a month table by repeatedly calling create_row until
# the whole month has been gone through.
# Returns a raw HTML string containing the table.

def create_month_table(year, month, calendar, user):
    thisDate = datetime.date(year,month,1)
    calendarString = "<table>"
    # count is for sanity safety.
    count = 0
    
    while (thisDate.month <= month and thisDate.year <= year) and count < 7:
        calendarString = calendarString + "<tr>"
        (newRow, newDate) = create_row(thisDate, calendar, user)
        calendarString = calendarString + newRow
        count = count + 1

        thisDate = newDate
        calendarString = calendarString + "</tr>"
        
    return calendarString + "</table>"


# create_row
# Creates a month table row:
# First takes modDate to be the previous Monday compared to thisDate
# (or thisDate if thisDate is Monday). Then iterates through weekdays,
# looks at their availability in the database and puts the cells in different
# classes. Puts also an id on them but it's not currently used. Also makes
# a onclick=toggle(...) javascript call for each cell, that will be used to
# toggle the availability.
# Returns a raw HTML string containing all this.

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



# ------- REQUEST HANDLERS ----------

# new_calendar
# Default page called for empty pattern ^$: Show a new_calendar template.

def new_calendar_request(request):
    context = {}
    return render(request, 'bandschedule/new_calendar.html', context)


# monthly_view
# Called for pattern /[0-9]*/ containing the calendar_id, returns
# a Http response using template monthly.html.

def monthly_view_request(request, calendar_id, year=None, month=None):
    
    if 'user' in request.session:
        username = request.session['user']
    else:
        username = None

    (year, month, c, user) = append_data(year, month, calendar_id, username)
    
    month_table = create_month_table(year, month, c, user)
    
    if month_table == None:
        return HttpResponse("")
    
    if month == 12:
        next_month = str(year+1) + "/1/"
    else:
        next_month = str(year) + "/" + str(month+1) + "/"

    if month == 1:
        prev_month = str(year-1) + "/12/"
    else:
        prev_month = str(year) + "/" + str(month-1) + "/"
    
    this_date = datetime.date(year,month,1)
    month_seen = MonthSeen.get_month_seen(this_date, c, user)
        
    month_seen_by = create_month_seen_by(this_date, c)

    if username == None:
        username = ""

    context = { 'calendar_id' : calendar_id, 'month_table' : month_table,
               'next_month': next_month, 'prev_month' : prev_month,
               'year': year, 'month': month, 'user': username,
               'month_seen': month_seen, 'month_seen_by': month_seen_by,
               'descstring': c.descstring }
    
    return render(request, 'bandschedule/monthly.html', context)

    
    
# login_user
# Called with login_user pattern.
# Sets the session parameter 'user' to be the 'user' string in the
# http request. Used with AJAX so response is not important.

def login_user_request(request):
    params = request.GET
    if 'user' not in params:
        return HttpResponse("")
#    print "Login", params['user']
    
    request.session['user'] = params['user']
    return HttpResponse("Ok")

# logout_user
# Called with logout_user pattern.
# Removes the session parameter 'user'.

def logout_user_request(request):
    if 'user' not in request.session:
        return HttpResponse("")

    del request.session['user']
    return HttpResponse("Ok")

# get_month
# Called with get_month pattern and called as an AJAX query from monthly.html.
# Fetches year, month and calendar_id parameter from the query and returns
# a JSON response having the contents of the calendar in that month.
# month_table will be an HTML formatted table that will be injected into the
# DOM where the calendar will be placed. 
# Month_seen will be a HTML formatted list of the users that have seen this month.
# It will be injected into the DOM as well. 


def get_month_request(request):
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

    (year, month, c, user) = append_data(year, month, calendar_id, username)

    month_table = create_month_table(year, month, c, user)
    this_date = datetime.date(year,month,1)
    month_seen = MonthSeen.get_month_seen(this_date, c, user)

    simple_data = { 'month' : month_table, 'month_seen' : month_seen }
    return HttpResponse(simplejson.dumps(simple_data), mimetype="application/json")

# approve_month_request
# Handles month_seen pattern. Gets the parameters from the request and calls
# approve_month to label the month as seen or not seen by the user, based on
# the yesno parameter.
# Returns a JSON object containing the new month_seen_by table reflecting the
# changed data.
    
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

        (year, month, c, user) = append_data(year, month, calendar_id, username)
        this_date = datetime.date(year,month,1)

        if (c == None):
            return HttpResponse("")
    

        approve_month(c, user, this_date, yesno)

        approve_table = create_month_seen_by(this_date, c)
        
        simple_data = { 'month_seen_by' : approve_table }
        
        return HttpResponse(simplejson.dumps(simple_data), mimetype="application/json")
    else:
        return HttpResponse("")

# create_calendar
# Called with create_calendar pattern.
# Creates a new calendar and redirects the response to monthly_view to show
# the user the contents of this calendar immediately.

def create_calendar_request(request):
    if request.method == 'POST':
        params = request.POST
        if 'descstring' in params:
            c = create_calendar(params['descstring'])
        
            return redirect('monthly_view', calendar_id=c.idstring)
        else:
            return HttpResponse("")
    else:
        return HttpResponse("")


# toggle_date
# Handles toggle_date pattern.
# Look at the contents, take targetyear, targetmonth and targetday request parameters
# and toggle the availability for that date for user in the session parameters and
# supplied calendar_id.
# Returns a JSON object containing a raw HTML table containing the new month data
# with the changed availability.

def toggle_date_request(request):
    if request.method == 'GET':
        params = request.GET
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
        
        (year, month, c, user) = append_data(year, month, calendar_id, username)

        if (c == None or user == None or targetyear == 0 or targetmonth == 0 or targetday == 0):
            return HttpResponse("")

        requestdate = datetime.date(targetyear, targetmonth, targetday)
#        print requestdate


        toggle_date(c, user, requestdate)
                    
        month_table = create_month_table(year, month, calendar_id, username)

        simple_data = { 'month' : month_table }
        
        return HttpResponse(simplejson.dumps(simple_data), mimetype="application/json")
    else:
        return HttpResponse("")
            
