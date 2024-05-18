from django.shortcuts import render
from psycopg2 import sql
from pacilflix.database_manager import DatabaseManager
import daftarkontributor.queries
from django.shortcuts import render

def show_daftarkontributor(request):
    kontributor = [] # array kontributor

    try:
        tipe = request.GET.get('tipe', 'all') # ambil sesuai tipe, kalo gak berarti dia all
        cursor = DatabaseManager.get_dict_cursor() # buka database

        if tipe in ['pemain', 'sutradara', 'penulis_skenario']: # kalo tipenya ada (bukan all)
            cursor.execute(sql.SQL(daftarkontributor.queries.contributors_by_type_query).format(table=sql.Identifier(tipe))) # execute query trus di-format sesuai tipe
        else: # kalo dia all
            tipe = 'all'
            cursor.execute(daftarkontributor.queries.contributors_all_query) # execute query

        kontributor = cursor.fetchall() # abis dibedain tipe sama all, baru fetch semua
        cursor.close() # close cursor

    except Exception as e: # kalo ada error
        DatabaseManager.rollback()
        print(e)

    return render(request, "daftarkontributor.html", {'kontributor': kontributor})
