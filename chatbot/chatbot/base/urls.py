from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name='home'),  # Home page
    path('login/', views.LoginPage, name='login'),  # Login page
    path('signup/', views.SignupPage, name='signup'),  # Signup page
    path('index/', views.index, name='index'),  # Index page
    path('chatbot/', views.chatbot_view, name='chatbot_view'),  # Chatbot view
]
