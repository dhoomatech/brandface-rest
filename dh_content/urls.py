from django.shortcuts import render

# Create your views here.
from django.urls import path

from . import views
from django.views.generic import TemplateView
urlpatterns = [
        # path('',TemplateView.as_view(template_name='dh_content/brandface.html')),
        # path('<str:url_type>', views.BranfaceIndex.as_view(), name='brandface_index'),
        # path('grocery-store', views.BranfaceIndexStore1.as_view(), name='brandface_index'),
        # path('home/', views.BranfaceHome.as_view(), name='brandface_home'),
]