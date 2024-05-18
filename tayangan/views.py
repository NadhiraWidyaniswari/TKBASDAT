from django.shortcuts import render
from pacilflix.database_manager import DatabaseManager
import tayangan.queries as queries
import math as Math
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

def show_tayangan(request):
    tayangan_terbaik = []
    films = []
    series = []
    try:
        range = request.GET.get('range', 'Global')
        print(range)
        cursor = DatabaseManager.get_dict_cursor()

        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            if range == "Lokal":
                cursor.execute(queries.GET_TAYANGAN_TERBAIK_LOCAL_LOGIN, (username,))
            else:
                cursor.execute(queries.GET_TAYANGAN_TERBAIK)
        else:
            if range == "Lokal":
                cursor.execute(queries.GET_TAYANGAN_TERBAIK_LOCAL_GUEST, ("indonesia",)) #default indonesia ajah
            else:
                cursor.execute(queries.GET_TAYANGAN_TERBAIK)

        tayangan_terbaik_temp = cursor.fetchall()

        cursor.execute(queries.GET_ALL_FILM)
        films = cursor.fetchall()
        
        cursor.execute(queries.GET_ALL_SERIES)
        series = cursor.fetchall()
        
        cursor.close()
    except Exception as e:
        DatabaseManager.rollback()
        print(e)

    for (i, row) in enumerate(tayangan_terbaik_temp):
        row = dict(row)
        row['peringkat'] = i + 1
        tayangan_terbaik.append(row)

    context = {
        "tayangan_terbaik": tayangan_terbaik,
        "films": films,
        "series": series,
        "jenis": "Tayangan" if 'username' in request.COOKIES else "Trailer"
    }
    return render(request, "tayangan.html", context=context)

def show_result(request):
    try:
        searchkey = request.GET.get('q', '')
        cursor = DatabaseManager.get_dict_cursor()
        cursor.execute(queries.SEARCH_TAYANGAN, {
                       'searchkey': f'%{searchkey}%', })
        tayangan = cursor.fetchall()
        cursor.close()
    except Exception as e:
        DatabaseManager.rollback()
        print(e)
    return render(request, "pencarian_tayangan.html", {"tayangan": tayangan})


def show_film(request, id):
    film = {}
    ulasan = {}
    try:
        cursor = DatabaseManager.get_dict_cursor()
        cursor.execute(queries.GET_FILM_BY_ID, (id,))
        film = cursor.fetchone()
        cursor.execute(queries.GET_SUTRADARA, (film.pop('id_sutradara'),))
        film['sutradara'] = cursor.fetchone()
        cursor.execute(queries.GET_GENRE, (id,))
        film['genres'] = cursor.fetchall()
        cursor.execute(queries.GET_PEMAIN, (id,))
        film['pemain'] = cursor.fetchall()
        cursor.execute(queries.GET_PENULIS_SKENARIO, (id,))
        film['penulis_skenario'] = cursor.fetchall()

        current_user_review = None
        
        cursor.execute(queries.GET_ULASAN, (id,))
        reviews = cursor.fetchall()
        ulasan = {
            "reviews": reviews,
            #"current_user_review": current_user_review
        }
        cursor.close()
    except Exception as e:
        DatabaseManager.rollback()
        print(e)
    return render(request, "film.html", {"film": film, "ulasan": ulasan})


def show_series(request, id):
    series = {}
    ulasan = {}

    try:
        cursor = DatabaseManager.get_dict_cursor()
        cursor.execute(queries.GET_SERIES_BY_ID, (id,))
        series = cursor.fetchone()
        cursor.execute(queries.GET_EPISODES_OF_SERIES, (id,))
        series['episodes'] = cursor.fetchall()
        cursor.execute(queries.GET_SUTRADARA, (series.pop('id_sutradara'),))
        series['sutradara'] = cursor.fetchone()
        cursor.execute(queries.GET_GENRE, (id,))
        series['genres'] = cursor.fetchall()
        cursor.execute(queries.GET_PEMAIN, (id,))
        series['pemain'] = cursor.fetchall()
        cursor.execute(queries.GET_PENULIS_SKENARIO, (id,))
        series['penulis_skenario'] = cursor.fetchall()

        current_user_review = None
        cursor.execute(queries.GET_ULASAN, (id,))
        reviews = cursor.fetchall()
        ulasan = {
            "reviews": reviews,
            #"current_user_review": current_user_review
        }
        cursor.close()
    except Exception as e:
        DatabaseManager.rollback()
        print(e)
    return render(request, "series.html", {"series": series, "ulasan": ulasan})


def show_episode(request, id_series, subjudul):
    try:
        cursor = DatabaseManager.get_dict_cursor()
        cursor.execute(queries.GET_EPISODE_BY_SUBJUDUL, (id_series, subjudul))
        episode = cursor.fetchone()
        cursor.execute(queries.GET_OTHER_EPISODES, (id_series, subjudul))
        episode['other_episodes'] = cursor.fetchall()
        cursor.close()
    except Exception as e:
        DatabaseManager.rollback()
        print(e)
    return render(request, "episode.html", {"episode": episode})


@csrf_exempt
@require_POST
def add_riwayat_nonton(request):
    try:
        username = request.COOKIES.get('username')
        json_data = json.loads(request.body) 
        id_tayangan = json_data['id_tayangan']
        progress = json_data['progress']

        cursor = DatabaseManager.get_dict_cursor()
        cursor.execute(queries.GET_DURASI_TAYANGAN, {'id': id_tayangan})
        durasi_tayangan = cursor.fetchone()['durasi']
        progress_time = Math.ceil(progress * durasi_tayangan / 100)
        end_date_time = datetime.now()
        start_date_time = end_date_time - timedelta(minutes=progress_time)
        cursor.execute(queries.ADD_RIWAYAT_NONTON, (id_tayangan, username, start_date_time, end_date_time))
        DatabaseManager.commit()

    except Exception as e:
        DatabaseManager.rollback()
        print(e)
        return JsonResponse({"status": "error"}, status=500)

    return JsonResponse({"status": "success"})