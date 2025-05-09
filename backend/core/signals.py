import django.dispatch

user_registered = django.dispatch.Signal() 
profile_updated = django.dispatch.Signal()
payment_successful = django.dispatch.Signal() 
match_alert_triggered = django.dispatch.Signal()