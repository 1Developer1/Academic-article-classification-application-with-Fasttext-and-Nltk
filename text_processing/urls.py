from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('interests/',views.interests_request,name='interests'),
    path('texts',views.search,name='texts'),
    path('register/', views.register_request, name='register'),
    path('logout',views.logout_request,name='logout'),
]