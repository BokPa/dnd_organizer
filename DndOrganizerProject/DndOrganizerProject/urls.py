"""
URL configuration for DndOrganizerProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dnd_organizer_app import views as dnd_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dnd_views.CampaignsListView.as_view(), name="campaigns-list"),
    path('character/<int:character_id>/', dnd_views.CharacterSheetView.as_view(), name="character-sheet"),
    path('campaign/<int:campaign_id>/', dnd_views.CampaignView.as_view(), name="campaign-detail"),
    path('login/', dnd_views.LoginView.as_view(), name="login"),
    path('logout/', dnd_views.LogoutView.as_view(), name="logout"),
    path('registration/', dnd_views.AddUserView.as_view(), name="registration"),
    path('add-campaign/', dnd_views.AddCampaignView.as_view(), name="add-campaign"),
    path('add-character/', dnd_views.AddCharacterView.as_view(), name="add-character"),
    path('campaign/<int:campaign_id>/add-players/', dnd_views.AddPlayersView.as_view(), name="add-players"),
    path('character/<int:character_id>/add-character-to-campaign/', dnd_views.AddCharacterToCampaign.as_view(),
         name="add-character-to-campaign"),
    path('character/<int:character_id>/edit-character/', dnd_views.EditCharacterView.as_view(), name="edit-character"),
    path('campaign/<int:campaign_id>/plan_session/', dnd_views.PlanSessionView.as_view(), name='plan_session'),
]
