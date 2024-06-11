"""
URL configuration for EventManagment project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
#list event
    path('', views.EventListsView.as_view(), name='event-list'),
    path('event-organized-list', views.EventListsOrganizedView.as_view(), name='my-event-organized'),
    path('event-subscribe-list', views.EventListsSubscribedView.as_view(), name='my-event-subscribe'),

    path('event-subscribe/<int:pk>', views.EventSubscribeView.as_view(), name='event-subscribe'),
    path('event-unsubscribe/<int:pk>', views.EventUnscribeView.as_view(), name='event-unsubscribe'),
    path('event-organized-list/<int:pk>/edit', views.EditEventView.as_view(), name="event_edit"),
    path('event-delete/<int:pk>', views.EventDeleteView.as_view(), name='event-delete'),

    path('new', views.CreateEventView.as_view(), name="event_new"),
]
