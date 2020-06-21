from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth

# Create your views here.

def login(request):
    if not request.user.is_authenticated:
        if request.method =='POST':
            if request.POST['email'] and request.POST['password']:
                try:
                    user =User.objects.get(email =request.POST['email'])
                    auth.login(request,user)
                    if request.POST['next'] != '':
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('/')
                except User.DoesNotExist:
                    return render(request,'accounts/login.html',{'error': 'User Dosen\'t exists.'})
            else:
                return render(request,'accounts/login.html',{'error': 'Empty Fields'})
        else:
            return render(request,'accounts/login.html')
    else:
        return redirect('/')


def signup(request):
    if request.method =='POST':
        if request.POST['password'] ==request.POST['password2']:
            if request.POST['username'] and request.POST['email'] and request.POST['password']:
                try:
                    user =User.objects.get(email = request.POST['email'])
                    return render(request,'accounts/signup.html',{'error':"User Already Exists."})
                except User.DoesNotExist:
                    User.objects.create_user(
                        username = request.POST['username'],
                        email = request.POST['email'],
                        password = request.POST['password'],
                    )
                    messages.success(request,'SignUp Successful \n Login Here')
                    return redirect(login)
            else:
                return render(request,'accounts/signup.html',{'error':"Empty Fields."})
        else:
             return render(request,'accounts/signup.html',{'error':"Password\'s Don\'t match."})
    else:
        return render(request,'accounts/signup.html')



def logout(request):
    auth.logout(request)
    return redirect('/accounts/login')