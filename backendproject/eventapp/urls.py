from django.urls import path
from .views import UploadEventsView, SearchEventsView

urlpatterns = [
    path('upload/', UploadEventsView.as_view()),
    path('search/', SearchEventsView.as_view()),
]
