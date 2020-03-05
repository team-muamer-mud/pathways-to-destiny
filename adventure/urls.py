from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('getrooms', api.get_rooms),
    path('pusher_auth', views.pusher_auth, name='pusher_auth'),
]