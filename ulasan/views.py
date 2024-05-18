from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pacilflix.database_manager import DatabaseManager
import ulasan.queries as queries
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


def show_ulasan(request):
    return render(request, "ulasan.html")

@require_POST
@csrf_exempt
def create_ulasan(request):
    try:
        json_data = json.loads(request.body)
        id_tayangan = json_data.get('id_tayangan')
        username = request.COOKIES.get('username')
        deskripsi = json_data.get('deskripsi')
        rating = json_data.get('rating')

        cursor = DatabaseManager.get_cursor()
        cursor.execute(queries.CREATE_ULASAN, [
                       id_tayangan, username, rating, deskripsi])
        DatabaseManager.commit()
        cursor.close()
    except Exception as e:
        DatabaseManager.rollback()
        print(e)
        return JsonResponse({"status": "error", "message": "Terjadi kesalahan saat menambahkan ulasan. Anda telah menulis ulasan untuk tayangan ini!"}, status=500)
    return JsonResponse({"status": "success", "message": "Ulasan berhasil ditambahkan!"})