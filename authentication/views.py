from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import User 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import get_template, render_to_string
from django.template import Context
from .forms import UserRegisterForm, EditMyProfile, EditUserProfile, AddUser, ChangePassword
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.urls import reverse

def index(request, single_slug):
    """if single_slug == 'admin':
        redirect('login')
    elif single_slug =='home':
        redirect('home')
    elif single_slug == 'register/':
        redirect('authentication:login')
    else:
        redirect('single_slug')"""
    return HttpResponse("Aloha there!")

def home(request):
    return redirect("tutor:home")

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # for not email based authentication
            user = form.save(commit=True)
            user.is_active=True
            messages.success(request, f"you are now registered successfully!!!")

            return redirect('authentication:login')
            """
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('tinyapp/acc_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request,
                         'tinyapp/email_confirmatiMyProfilon.html')
            """

    else:
        form = UserRegisterForm()
    return render(request,
                  "authentication/register.html",
                  context={'form':form}) # must be tha same name as the one in register.html
        
# user will get activate link to their email address
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("/")
    else:
        return render(request,
                      "authentication/activation_expired.html")
@login_required
def logout_(request):
    logout(request)
    messages.info(request, "logged out successfully!")
    return redirect("authentication:login")

@never_cache
def login_(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tutor:home'))
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            UserModel = get_user_model()
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                messages.success(request, f"you are now logged in as {username}")
                return redirect("tutor:home")
            return redirect("authentication:login")
                
        form = AuthenticationForm()
        return render(request,
                    "authentication/login.html",
                    {'form':form}) # must be tha same name as the one in register.html
@login_required
def my_profile(request):
    if request.user:
        user = request.user
    initial_info = {'user':user}
    if request.method == 'POST':
        form = EditMyProfile(request.POST, request.FILES, instance=request.user, initial=initial_info)
        if form.is_valid():
            change = form.save(commit=False)
            change.save()
            messages.success(request, "The user "+change.username+" was updated successfully.")

    else:
        form = EditMyProfile(instance=request.user, initial=initial_info)
    return render(request,
                  "authentication/editMyProfile.html",
                  {'form':form})
@login_required
def change_password(request):
    print(request.method)
    if request.method == 'POST':
        print("Aloha")
        form = ChangePassword(request.POST, password=request.user.password)
        if form.is_valid():
            print(True)
            new_password = request.POST.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "The password was changed successfully.")
    else:
        form = ChangePassword(password=request.user.password)

    return render(request,
                  "authentication/changePassword.html",
                  {'form':form})