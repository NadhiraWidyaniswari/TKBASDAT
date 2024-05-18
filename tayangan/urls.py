from django.urls import path
from tayangan.views import *

app_name = 'tayangan'

urlpatterns = [
    path('', show_tayangan, name='show_tayangan'),
    path('pencarian', show_result, name='show_result'),
    path('detail-film/<str:id>', show_film, name='show_film'),
    path('detail-series/<str:id>', show_series, name='show_series'),
    path('detail-episode/<str:id_series>/<str:subjudul>',show_episode, name='show_episode'),
    path('tonton', add_riwayat_nonton, name='add_riwayat_nonton')
]