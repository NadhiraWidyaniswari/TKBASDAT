import json
from django.http import JsonResponse
from django.shortcuts import render
from pacilflix.database_manager import DatabaseManager
import langganan.queries as queries
from django.views.decorators.csrf import csrf_exempt

def show_langganan(request):
    context = {} # buat isi halaman

    username = request.COOKIES.get('username') # ambil username

    try:
        cursor = DatabaseManager.get_dict_cursor() # buka database
        cursor.execute(queries.current_subscription_query, (username,)) # execute query dengan parameter username
        current_subscription = cursor.fetchone() # ambil 1 data dari database

        if current_subscription: # kalo ada yang diambil (ada paket aktif)
            nama_paket = current_subscription.get('nama', '') # ambil namanya
        else: # kalo gaada yang diambil (gaada paket aktif)
            nama_paket = '' # nama blank

        cursor.execute(queries.other_subscriptions_query, (nama_paket,)) # execute query dengan parameter nama_paket
        other_subscriptions = cursor.fetchall() # ambil seluruh data dari database
        cursor.execute(queries.history_of_subscriptions_query, (username,)) # execute query dengan parameter username
        history_of_subscriptions = cursor.fetchall() # ambil seluruh data dari database

        context = { # isi halamannya pake data yang udah diambil
            'current_subscription': current_subscription,
            'other_subscriptions': other_subscriptions,
            'history_of_subscriptions': history_of_subscriptions,
        }

        cursor.close() # close cursor

    except Exception as e: # kalo ada error
        DatabaseManager.rollback()
        print(e)
    
    return render(request, "langganan.html", context)

@csrf_exempt # csrf exempt buat keamanan akses
def show_beli(request):
    if request.method == 'POST': # kalo method aksesnya post

        try:
            username = request.COOKIES.get('username') # ambil username
            json_data = json.loads(request.body) # sesuai sama request, ambil data dari yang dipilih
            nama_paket = json_data.get('nama_paket') # ambil data nama_paket dari request
            metode_pembayaran = json_data.get('metode_pembayaran') # ambil data metode_pembayaran request

            cursor = DatabaseManager.get_dict_cursor() # buka database
            cursor.execute(queries.current_subscription_query, (username,)) # execute query dengan parameter username
            current_subscription = cursor.fetchone() # ambil 1 data dari database

            if current_subscription: # kalo ada yang diambil (ada paket aktif)
                cursor.execute(queries.update_subscription_query, {
                    'username': username,
                    'metode_pembayaran': metode_pembayaran,
                    'nama_paket': nama_paket,
                }) # execute query pake parameter itu dan isinya sesuai sama yang udah diambil

            else: # kalo gaada yang diambil (gaada paket aktif)
                cursor.execute(queries.create_transaction_query, (username, nama_paket, metode_pembayaran)) # execute query pake parameter yang udah diambil

            DatabaseManager.commit() # di-update database-nya
            cursor.close() # close cursor
            return JsonResponse({'status': 'success', 'message': 'Pembelian berhasil!'}) # kalo berhasil, keluar pesan
        
        except Exception as e: # kalo ada error
            DatabaseManager.rollback()
            print(e)
            return JsonResponse({'status': 'failed', 'message': 'Pembelian gagal!'}, status=500)
        
    else: # kalo request bukan POST
        context = {}  # buat isi halaman

        try:
            nama_paket = request.GET.get('paket') # ambil nama paket sesuai yang di-request
            cursor = DatabaseManager.get_dict_cursor() # buka database
            cursor.execute(queries.get_paket_query, [nama_paket]) # execute query pake parameter nama_paket
            paket = cursor.fetchone() # ambil 1 data dari nama_paket
            cursor.close() # close cursor

            context = { # isi halamannya pake data yang udah diambil
                'paket': paket,
            }  

        except Exception as e: # kalo ada error
            DatabaseManager.rollback()
            print(e)

        return render(request, 'beli.html', context)
