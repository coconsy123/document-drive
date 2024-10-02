from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from decorators.decorators import unauthenticated_user
from frontend.models import Account
from frontend.forms import RegistrationForm
from frontend.utils import password_checker
import requests
from django.conf import settings


@login_required
def index_page(request):
    try:
        pass
    except Exception as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)




@unauthenticated_user
def login_page(request):
    if request.user.is_authenticated:
        return redirect('backend-index-page')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        account = Account.objects.filter(email=email).first()
        # Verify reCAPTCHA
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            return JsonResponse({'error': True, 'msg': 'Invalid reCAPTCHA. Please try again.'})
        
        if account:
            user = authenticate(email=email, password=password, request=request)
            if user:
                login(request, user)
                return JsonResponse({'data': 'success'})  # Return token in response
            else:
                return JsonResponse({'error': True, 'msg': 'Wrong password. Try again'})
        else:
            return JsonResponse({'error': True, 'msg': "Couldn't find your account"})
    
    return render(request, 'frontend/login/login.html', {
        'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY
    })

@unauthenticated_user
def register_page(request):
    try:
        context = {
            'form': RegistrationForm()
        }
        if request.user.is_authenticated:
            return redirect('dashboard')
        if request.method == "POST":
            with transaction.atomic():
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    password = form.clean_password()
                    firstname = form.cleaned_data['firstname']
                    lastname = form.cleaned_data['lastname']
                    middlename = form.cleaned_data['middlename']
                    new_account = Account.objects.create_user(email=email, password=password)
                    account = Account.objects.filter(id=new_account.id).update(firstname=firstname,
                                                                               middlename=middlename, lastname=lastname,
                                                                               is_admin=True)

                    return JsonResponse({'statusMsg': 'Account successfully created.'}, status=200)
                else:
                    return JsonResponse({'statusMsg': form.errors}, status=404)

        return render(request, 'frontend/register/register.html', context)

    except Exception as e:
        return JsonResponse({'statusMsg': str(e)}, status=404)
    

def logout_page(request):
    logout(request)
    return redirect('frontend-login')