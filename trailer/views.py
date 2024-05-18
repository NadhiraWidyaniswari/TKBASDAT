from django.shortcuts import render

def show_trailer(request):
    return render(request, "trailer.html")

def show_result(request):
    return render(request, "pencarian.html")