from django.urls import path
from publications import views

urlpatterns = [
    path('publications/', views.PublicationList.as_view()),
    path('publications/<int:pk>/', views.PublicationDetail.as_view()),
]