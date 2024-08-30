from django.urls import path
from . import views
from tj.views import IndexView,HomeView



urlpatterns = [
    path('', HomeView.as_view()),
    path('analyze', IndexView.as_view()),
   
]