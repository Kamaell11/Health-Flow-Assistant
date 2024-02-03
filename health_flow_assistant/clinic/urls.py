# clinic/urls.py
from django.urls import path
from .views import home, contact, logout_view
app_name = 'clinic'
urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('logout/', logout_view, name='logout'),
]
