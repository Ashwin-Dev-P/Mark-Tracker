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
    path('additionalInfo',views.additionalInfoFunction,name="additionalInfo"),
    path('edit',views.edit,name="edit"),

]