from django.shortcuts import render,redirect
from django.contrib.auth import *
from django.contrib.auth.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import *
import datetime
from pacilflix.database_manager import DatabaseManager
import authentication.queries as queries



def show_authentication(request):
    return render(request, "authentication.html")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            cursor = DatabaseManager.get_dict_cursor()
            cursor.execute(queries.LOGIN, [username, password])
            user = cursor.fetchone()
        except Exception as e:
            DatabaseManager.rollback()
            print(e)
            messages.error(
                request, 'Sorry, something went wrong. Please try again later.')

        if user is not None:
            response = HttpResponseRedirect(reverse("tayangan:show_tayangan"))
            response.set_cookie('is_authenticated', True)
            response.set_cookie('username', username)
            return response
        else:
            messages.info(
                request, 'Sorry, incorrect username or password. Please try again.')

    context = {}
    return render(request, 'login.html', context)

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password1')
        negara_asal = request.POST.get('country')

        try:
            cursor = DatabaseManager.get_dict_cursor()
            cursor.execute(queries.REGISTER, [username, password, negara_asal])
            DatabaseManager.commit()
        except Exception as e:
            DatabaseManager.rollback()
            print(e)
            messages.error(
                request, 'Sorry, something went wrong. Please try again later.')
            return redirect('authentication:register')
        
        messages.success(
            request, 'Your account has been successfully created!')
        return redirect('authentication:login')
    
    form = RegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context)

@csrf_exempt
def logout(request):
    response = HttpResponseRedirect(reverse("authentication:show_authentication"))
    response.delete_cookie('is_authenticated')
    response.delete_cookie('username')
    return response