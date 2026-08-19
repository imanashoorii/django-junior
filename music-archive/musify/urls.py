from django.urls import path

from musify.views import list_create_view, retrieve_update_delete_view

urlpatterns = [
    path('', list_create_view, name="musify-list"),
    path('<int:pk>/', retrieve_update_delete_view, name="musify-detail"),
]
