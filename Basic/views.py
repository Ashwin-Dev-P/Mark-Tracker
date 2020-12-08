from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from Basic.models import markDetails
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html',{'title':'MarkTracker'})

def signUp(request):
    if(request.method == "GET"):
        return render(request,"signUp.html",{'title':'Sign Up'})
    elif(request.method == "POST"):
        username = request.POST['username']
        if(User.objects.filter(username=username).exists()):
            messages.info(request,'Username is taken')
            return redirect('SignUp')
        email = request.POST['email']
        if(User.objects.filter(email=email).exists()):
            messages.info(request,"E-mail is already in use.")
            return redirect('SignUp')
        
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 != password2):
            messages.info(request,"Both the passwords do not match.")
            return redirect('SignUp')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        user = User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
        user.save()
        print("User account is created.")
        messages.info(request,"Account created successfully.")
        auth.login(request,user)
        return redirect('main')



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
        data = markDetails.objects.filter(user_id=request.user.id)
        return render(request,"main.html",{'title':'main','data':data})
    else:
        messages.info(request,"Login to continue.")
        #return render(request,"login,html")
        return redirect('login')
def logOut(request):
    auth.logout(request)
    return redirect('/')

def add(request):
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            return render(request,"add.html",{'title':'Add'})
        else:
            return redirect("login")
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











