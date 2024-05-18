from django.urls import path
from trailer.views import *

app_name = 'trailer'

urlpatterns = [
    path('', show_trailer, name='show_trailer'),
    path('pencarian', show_result, name='show_result'),
]