

  Band scheduler / Band planner
  
  Copyright 2012-2013 Teppo Kankaanpää
  
  
  1. Introduction
  
    This is a Python Django application for a very specific scheduling
  problem detailed in templates/bandschedule/new_calendar.html,
  the root page of the application.
  
    The application follows Django standards: The models are laid out in
  bandschedule/models.py and the bulk of the code is in bandschedule/views.py.
  Template htmls reside in templates/bandschedule.
  
  2. Deployment
  
    Set the correct path to the project in apache/django.wsgi and point Apache
  to this file.
  
    Create a database of your choice and change settings in bandplanner/settings.py
  to reflect this. Point the template directory in bandplanner/settings.py to the
  correct location.
  
    Get your own random secret key and put it to bandplanner/settings.py. It's a
  70ish character string of standard ASCII characters.
  
  
