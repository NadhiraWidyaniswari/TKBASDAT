from django.shortcuts import render

def show_pengguna(request):
    return render(request, "pengguna.html")