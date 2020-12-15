from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from Basic.models import markDetails,Departments,additionalInfo
from django.contrib import messages
from Basic.forms import UserForms,MarkForms,infoForms
from django.http import HttpResponse
from django.urls import reverse

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
        if(markDetails.objects.filter(user_id=request.user.id).exists()):

            data_present = 1;
        else:
            data_present = 0;
        return render(request,"main.html",{'title':'main','data':data,'data_present':data_present})
    else:
        messages.error(request,"Login to continue.")
        return redirect('login')

def delete(request,id):
    dataToBeDeleted = markDetails.objects.get(id=id)
    dataToBeDeleted.delete()
    return redirect('main')

def edit_marks(request,id):
    if(request.method == "GET"):
        markDetailsToBeEdited = markDetails.objects.get(id=id)
        semesters = range(1,9)
        
        return render(request,"edit_marks.html",{'mark_details':markDetailsToBeEdited,'semesters':semesters})
    if(request.method == "POST"):
        
        dataToBeEdited = markDetails.objects.get(id=id)
        form = MarkForms(request.POST,instance=dataToBeEdited)
        if(form.is_valid()):
            form.save()
            messages.success(request,'Marks updated.')
            
        else:
            messages.error(request,"Invalid form data.")
        return redirect('main')
    else:
        messages.error(request,"Only get method request will be handled.")
        return render(request,"NotFound")

def edit_marks_post(request,id):
    if(request.method == "POST"):
        dataToBeEdited = markDetails.objects.get(id=id)
        form = MarkForms(request.POST,instance=dataToBeEdited)
        if(forms.is_valid()):
            form.save()
            messages.success('Marks updated.')
            return redirect('main')
        else:
            messages.error(request,"Inform form data.")
            return redirect("edit_marks")
    else:
        messages.error(request,"Only post methods will be handled.")
        return redirect("edit_marks.html")
    


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
    
    if(request.method == "GET"):
        
        if(request.user.id is None):
            messages.error(request,"Login to continue.")
            return redirect('login')
        
        details = User.objects.get(id=request.user.id)

        if(additionalInfo.objects.filter(user_id=request.user.id).exists()):
            additionalInfoObjects = additionalInfo.objects.filter(user_id=request.user.id).first()
            department_object = Departments.objects.get(id=additionalInfoObjects.Department_id)
            department_name = department_object.name
            current_semester = additionalInfoObjects.current_semester_id
            if(additionalInfoObjects.privacy == 0):
                privacy = "Private"
            else:
                privacy = "Public"
        else:
            department_name = "";
            privacy = "Private";
            current_semester = 1;

        
        
        return render(request,"profile.html",{'title':'Profile','details':details,'current_semester':current_semester,'department_name':department_name,'privacy':privacy})
    else:
        return HttpResponse("Only Post and Get request will be handled.")




def edit(request):
    if(not request.user.is_authenticated):
        messages.error(request,"Login to continue.")
        return redirect('login')
    else:
        if(request.method == "GET"):
            details = User.objects.get(id=request.user.id)
            departments = Departments.objects.all()

            if(additionalInfo.objects.filter(user_id = request.user.id).exists()):
                additionalInfoObjects = additionalInfo.objects.filter(user_id=request.user.id).first()
                department_object = Departments.objects.get(id=additionalInfoObjects.Department_id)
                department_name = department_object.name
                current_sem = additionalInfoObjects.current_semester_id
                privacy = additionalInfoObjects.privacy
            else:
                department_name = "";
                current_sem = 1;
                privacy = 0;
            
            semesters = range(1,9)
            #print("Department name:",department_name)
            return render(request,"edit.html",{'title':'edit','details':details,'departments':departments,'department_name':department_name,"current_semester":current_sem,"semesters":semesters,'privacy':privacy})
        elif(request.method == "POST"):

            #User details form.
            update = User.objects.get(id=request.user.id)
            form = UserForms(request.POST,instance=update)
            if(form.is_valid()):
                form.save()
                messages.success(request,"Record Updated")
                print("Record profile Updated.")
                
            else:
                messages.error(request,"Form is invalid.")
                return redirect('edit')


            department = request.POST.get('Department',"Computer Science")
            sem = request.POST.get('current_semester',"4")
        
            if( not Departments.objects.filter(name=department).exists()):
                departmentToBeAdded = Departments(name=department)
                departmentToBeAdded.save()
                messages.info(request,"New department added")
            department_id = Departments.objects.filter(name=department).first()
            post = request.POST.copy()
            post['Department'] = department_id.id
            request.POST = post
            print(post['Department'],request.POST['Department'])

        
        
            if( additionalInfo.objects.filter(user_id=request.user.id).exists()):
                additionalInfoUpdate = additionalInfo.objects.filter(user_id=request.user.id).first()
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
            messages.error(request,"This request method cannot be accessed.")
            return redirect("NotFound")
        return redirect('profile')
def notFound(request):
    return render(request,"NotFound.html",{'title':'Not Found'})
def logOut(request):
    auth.logout(request)
    return redirect('/')