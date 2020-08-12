from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
     path('tourdetails/', views.TournamentDetails.as_view(),name="Tournament View"),

     path('tourdetails/<tourid>/', views.InduvialTournamentDetails.as_view(),name="InvidiualTournament View"),

     path('registertour/', views.RegisterTournamentView.as_view(),name="RegisterTournament View"),
     path('generate/', views.TournamentGenerate.as_view(),name="Tournament Generate View"),
    ]