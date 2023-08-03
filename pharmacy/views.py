from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime


# Create your views here.

def index(request):
    return render(request, template_name="pharmacy/index.html")


def loginPage(request):
    if request.user.is_authenticated:
        # if request.user.is_superuser:
        #     return redirect(to='/admin')
        redirect(to='/home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            # if user.is_superuser:
            #     return redirect(to='/admin')
            return redirect(to='/home')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {'messages': messages.get_messages(request), 'currentYear': datetime.now().year}
    return render(request=request, template_name='pharmacy/index.html', context=context)


def logout_view(request):
    logout(request)
    return redirect(to='login')


@login_required(login_url='login')
def home(request):
    context = {'currentYear': datetime.now().year}
    return render(request=request, template_name='pharmacy/home.html', context=context)
