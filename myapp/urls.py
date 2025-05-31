from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index,name="Main"),
    path("booking/<int:myid>", views.booking, name="booking"),
    path("signin/", views.signup_view, name="Sign-In"),
    path("login/", views.login_view, name="Log-In"),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_form, name='ContactForm'),
    path('profile/', views.profile_view, name='Profile'),
    path('hotels/', views.hotels, name='hotels'),
    path('todo/', views.todo, name='todo'),
    path('restaurants/', views.restaurants, name='restaurants'),
    path('flights/', views.flights, name='flights'),
    path('holiday-home/', views.holiday_home, name='holiday-home'),
    path('reviews/', views.reviews, name='reviews'),
    path('basic/', views.basic, name='basic'),
    path('luxury/', views.luxury, name='luxury'),
    path('family/', views.family, name='family'),
    path('weekend/', views.weekend, name='weekend'),
    path('all/', views.all, name='all'),
    path('feedback/', views.feedback, name='feedback'),
    path('search/', views.search, name="search"),
    path('day/', views.day, name="day"),
    path('days/', views.days, name="days"),
    path('festive/', views.festive, name="festive"),
    path('international/', views.international, name="international"),
    path('national/', views.national, name="national"),
    path('dream/', views.dream, name="dream"),
    path('m/', views.m, name="m"),
    path('b/', views.b, name="b"),
    path('a/', views.a, name="a"),
    path('p/', views.p, name="p"),
    path('h/', views.h, name="h"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)