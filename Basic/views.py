from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from Basic.models import markDetails,Departments,additionalInfo
from django.contrib import messages
from Basic.forms import UserForms,MarkForms,infoForms
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html',{'title':'MarkTracker'})

def signUp(request):
    if(request.method == "GET"):
        return render(request,"signUp.html",{'title':'Sign Up'})
    elif(request.method == "POST"):
        username = request.POST['username']
        if(User.objects.filter(username=username).exists()):
            messages.error(request,'Username is taken')
            return redirect('SignUp')
        email = request.POST['email']
        if(User.objects.filter(email=email).exists()):
            messages.error(request,"E-mail is already in use.")
            return redirect('SignUp')
        
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 != password2):
            messages.error(request,"Both the passwords do not match.")
            return redirect('SignUp')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        user = User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
        user.save()
        print("User account is created.")
        messages.success(request,"Account created successfully.")
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
            messages.error(request,'Invalid credentials.')
            return render(request,"logIn.html",{'title':'login'})

def main(request):
    if(request.user.is_authenticated):
        data = markDetails.objects.filter(user_id=request.user.id)
        return render(request,"main.html",{'title':'main','data':data})
    else:
        messages.error(request,"Login to continue.")
        return redirect('login')


def add(request):
    if(request.method == 'GET'):
        if(request.user.is_authenticated):
            return render(request,"add.html",{'title':'Add'})
        else:
            messages.error(request,"login to continue.")
            return redirect("login")
    elif(request.method == "POST"):
        semester = request.POST['semester']
        subject_name = request.POST['subject_name']
        marks = request.POST['marks']
        mark_details = markDetails(semester=semester,subject_name=subject_name,marks=marks,user_id=request.user.id)
        mark_details.save()
        messages.success(request,"Marks added.")
        return redirect('main')

def profile(request):
    #departments = Departments.objects.all()
    if(request.method == "GET"):
        
        if(request.user.id is None):
            messages.error(request,"Login to continue.")
            return redirect('login')
        
        details = User.objects.get(id=request.user.id)
        additionalInfoObjects = additionalInfo.objects.get(id=request.user.id)
        department_object = Departments.objects.get(id=additionalInfoObjects.Department_id)
        department_name = department_object.name
        return render(request,"profile.html",{'title':'Profile','details':details,'additionalinfo':additionalInfoObjects,'department_name':department_name})
    else:
        return HttpResponse("Only Post and Get request will be handled.")

def additionalInfoFunction(request):
    if(request.method == "POST"):
        
        department = request.POST['Department']
        
        sem = request.POST['current_semester']
        isstr = isinstance(department, str)
        if(isstr or not Departments.objects.filter(id=department).exists()):
            departmentToBeAdded = Departments(name=department)
            departmentToBeAdded.save()
            messages.info(request,"New department added")
            department_id = Departments.objects.filter(name=department).first()
            post = request.POST.copy()
            post['Department'] = department_id.id
            request.POST = post
            print(post['Department'],request.POST['Department'])

        
        
        if( additionalInfo.objects.filter(id=request.user.id).exists()):
            additionalInfoUpdate = additionalInfo.objects.filter(id=request.user.id).first()
            if(additionalInfoUpdate is None):
                messages.error(request,"No additional info is found for the user.")
                return redirect("edit")
            
            infoForm = infoForms(request.POST,instance=additionalInfoUpdate)

            if(infoForm.is_valid()):
                infoForm.save()
                messages.success(request,"Department and semester updated.")
                print("Dept and sem success")
                return redirect('profile')
            else:
                #printf.errors
                print(infoForm.errors)
                messages.error(request,"Department and semester is not updated.")
                return redirect("edit")
        else:
            department_object= Departments.objects.get(name=department)
            #return render(request,"edit.html",{'obj':department_object})

            otherInfo = additionalInfo(Department_id=department_object.id,current_semester_id=sem,user_id=request.user.id)
            otherInfo.save()
        messages.success(request,"Department updated.")
        print("Department updated.")
    else:
        messages.error(request,"additionalInfo page cannot be accessed.")
    return redirect('profile')
    


def edit(request):
    if(not request.user.is_authenticated):
        messages.error(request,"Login to continue.")
        return redirect('login')
    else:
        if(request.method == "GET"):
            details = User.objects.get(id=request.user.id)
            departments = Departments.objects.all()

            return render(request,"edit.html",{'title':'edit','details':details,'departments':departments})
        elif(request.method == "POST"):

            #User details form.
            update = User.objects.get(id=request.user.id)
            form = UserForms(request.POST,instance=update)
            if(form.is_valid()):
                form.save()
                messages.success(request,"Record Updated")
                print("Record profile Updated.")
                #return redirect('profile')
            else:
                messages.error(request,"Form is invalid.")
                return redirect('edit')

            
            #Additional info form.
            department = request.POST['Department']
            sem = request.POST['current_semester']            
            if(not Departments.objects.filter(name=department).exists()):
                departmentToBeAdded = Departments(name=department)
                departmentToBeAdded.save()
                #otherInfo = additionalInfo.objects.get(id=request.user.id)
            if(additionalInfo.objects.filter(user_id=request.user.id).exists()):

                additionalInfoUpdate = additionalInfo.objects.get(user_id=request.user.id)
                if(additionalInfoUpdate is None):
                    messages.error(request,"No additional info is found for the user.")

                    return redirect("edit")
                print("dept id=",additionalInfoUpdate.Department_id)
                infoForm = infoForms(request.POST,instance=additionalInfoUpdate)

                if(infoForm.is_valid()):
                    infoForm.save()
                    message.success(request,"Department and semester updated.")
                    print("Dept and sem success")
                    return redirect('profile')
                else:
                    #printf.errors
                    messages.error(request,"Department and semester is not updated.")
                    return redirect("edit")
            else:
                department_object= Departments.objects.get(name=department)
                #return render(request,"edit.html",{'obj':department_object})

            otherInfo = additionalInfo(Department_id=department_object.id,current_semester_id=sem,user_id=request.user.id)
            otherInfo.save()
            messages.success(request,"Department updated.")
            print("Department updated.")
            

            
       
        
        return render(request,"profile.html",{'title':'Profile'})
        return render(request,"edit.html",{'title':'edit','details':details})


def logOut(request):
    auth.logout(request)
    return redirect('/')


    
        











