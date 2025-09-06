from django.urls import path
from . import views

app_name = 'edit'

urlpatterns = [
    path("add/", views.add_quote, name="add_quote"),
    path("change/<int:id>/", views.change_quote, name="change_quote"),
    path("delete/<int:id>/", views.delete_quote, name="delete_quote"),
]
