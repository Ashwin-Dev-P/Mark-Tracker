from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from .models import markDetails

# Create your views here.
def index(request):
    return render(request,'index.html',{'title':'home'})

def signUp(request):
    return render(request,"signUp.html",{'title':'Sign Up'})

def logIn(request):
    if(request.method == "GET"):
        return render(request,"logIn.html",{'title':'login'})
    elif(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('main')
        else:
            return render(request,"logIn.html",{'title':'login'})
def main(request):
    if(request.user.is_authenticated):
        return render(request,"main.html",{'title':'main'})
    else:
        return redirect('login')
def logOut(request):
    auth.logout(request)
    return redirect('/')

def add(request):
    if(request.method == 'GET'):
        return render(request,"add.html",{'title':'Add'})
    elif(request.method == "POST"):
        Department = request.POST['Department']
        semester = request.POST['semester']
        subject_name = request.POST['subject_name']
        marks = request.POST['marks']
        mark_details = markDetails(Department=Department,semester=semester,subject_name=subject_name,marks=marks)
        instance = mark_details
        instance.user = request.user
        instance.save()
        print('Mark details are added.')
        return redirect('main')











