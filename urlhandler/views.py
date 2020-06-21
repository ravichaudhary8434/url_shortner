from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shorturl
import random,string


# Create your views here.

@login_required(login_url ='/accounts/login')
def dashboard(request):
    usr =request.user
    urls =Shorturl.objects.filter(user =usr)
    return render(request,'urlhandler/dashboard.html',{'urls':urls})


def randomgen():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(6))



@login_required(login_url ='/accounts/login')
def generate(request):
    if request.method =='POST':
        #generate
        if request.POST['original'] and request.POST['short']:
            usr =request.user
            original =request.POST['original']
            short =request.POST['short']
            check =Shorturl.objects.filter(short_query =short)
            if not check:
                newurl =Shorturl(
                    user =usr,
                    original_url =original,
                    short_query =short,
                )
                newurl.save()
                return redirect('/urlhandler/dashboard')
            else:
                messages.error(request, 'Already Exists.')
                return redirect('/urlhandler/dashboard')

        elif request.POST['original']:
            #generate randomly
            usr =request.user
            original =request.POST['original']
            generated =False
            while not generated:
                short =randomgen()
                check =Shorturl.objects.filter(short_query =short)
                if not check:
                    newurl =Shorturl(
                        user =usr,
                        original_url =original,
                        short_query =short,
                    )
                    newurl.save()
                    return redirect('/urlhandler/dashboard')
                else:
                    continue
        else:
            messages.error(request, 'Empty Fields.')
            return redirect('/urlhandler/dashboard')
    else:
        return redirect('/urlhandler/dashboard')




def home(request,query=None):
    if not query or query is None:
        return render(request,'index.html')
    else:
        try:
            check =Shorturl.objects.get(short_query =query)
            check.visits +=1
            check.save()
            url_to_redirect =check.original_url
            return redirect(url_to_redirect)
        except Shorturl.objects.DoesNotExists:
            return render(request,'index.html',{'error':'error'})
    




@login_required(login_url='/accounts/login/')
def deleteurl(request):
    if request.method == "POST":
        short = request.POST['delete']
        try:
            check = Shorturl.objects.filter(short_query=short)
            check.delete()
            return redirect('/urlhandler/dashboard')
        except Shorturl.objects.DoesNotExists:
            return redirect('/')
    else:
        return redirect('/')
