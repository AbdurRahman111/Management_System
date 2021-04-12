from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth.hashers import make_password

# Create your views here.
from .models import CustomUser
from .forms import CustomUser_details

def demo(request):
    return render(request, 'demo.html')
def logins(request):
    return render(request, "login.html ")

def dl(request):
    if request.method != "POST":
        return HttpResponse(" not allowed ")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            else:
                return HttpResponseRedirect(reverse("student_home"))
               ## return HttpResponse("student login" + str(user.user_type))
            ##return HttpResponse("Email: " + request.POST.get("email") + "Password :" + request.POST.get("password"))
        else:
            messages.error(request, "Invalid Login Details")
            return render(request, "login.html ")

def det(request):      # detail user
    if request.user is not None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def signup_admin(request):
    return render(request, "signup_admin_page.html")

def signup_student(request):
    return render(request, "signup_student_page.html")

def do_admin_signup(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, user_type=1)
        user.save()
        messages.success(request, "Successfully Created Admin")
        return HttpResponseRedirect(reverse("login"))
    except:
        messages.error(request, "Failed to Create Admin")
        return HttpResponseRedirect(reverse("login"))


def PasswordReset(request):
    return render(request, 'password_reset_form.html')

def reset_password_email(request):
    reset_email=request.POST.get('reset_email')
    # print(reset_email)
    get_CustomUser = CustomUser.objects.get(email=reset_email)
    # print(get_CustomUser)

    get_id=get_CustomUser.id

    form=CustomUser_details()

    # if request.method=="POST":
    #     form = CustomUser_details(request.POST, instance=get_CustomUser)
    #     if form.is_valid():
    #         form.save()

    context3={'form':form, 'get_id':get_id}

    return render(request, 'password_reset_email.html', context3)

def reset_password_email_done(request):
    reset_email=request.POST.get('reset_email')
    print(reset_email)
    get_CustomUser = CustomUser.objects.get(id=reset_email)
    print(get_CustomUser)

    if request.method=="POST":
        form = CustomUser_details(request.POST, instance=get_CustomUser)
        if form.is_valid():
            form = form.save(commit=False)
            form.password = make_password(form.password)
            form.save()


    return render(request, 'password_reset_done.html')

