from django.urls import path
from ulasan.views import *

app_name = 'ulasan'

urlpatterns = [
    path('', show_ulasan, name='show_ulasan'),
    path('create/', create_ulasan, name='create_ulasan')
]