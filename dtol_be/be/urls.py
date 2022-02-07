from django.urls import path

from .views import SearchCategories

urlpatterns = [
    path('category/<str:query>/', SearchCategories.as_view()),
]
