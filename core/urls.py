from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/',views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('chat/', views.chat, name='chat'),
    path('ggml/', views.AI_GGML, name='ggml'),
    path('CargaDocumental/', views.CargaDocumental, name='CargaDocumental' ),
     
]
