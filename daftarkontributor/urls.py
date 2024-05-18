from django.urls import path
from daftarkontributor.views import show_daftarkontributor

app_name = 'daftarkontributor'

urlpatterns = [
    path('', show_daftarkontributor, name='show_daftarkontributor'),
]