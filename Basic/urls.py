from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="home"),
    path('signUp',views.signUp,name="SignUp"),
    path('logIn',views.logIn,name="login"),
    path('main',views.main,name="main"),
    path('logOut',views.logOut,name="logout"),
    path('add',views.add,name="add"),
    path('profile',views.profile,name="profile"),
    path('edit',views.edit,name="edit"),
    path('notFound',views.notFound,name="Not Found"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('edit_marks/<int:id>',views.edit_marks,name="edit_marks"),
    path('rank/<int:department_id>/<int:semester>/<str:subject_name>',views.rank,name="rank"),
    path('students',views.students,name="students"),
    
    

]