from django.urls import path
from pengguna.views import show_pengguna

app_name = 'pengguna'

urlpatterns = [
    path('', show_pengguna, name='show_pengguna'),
]