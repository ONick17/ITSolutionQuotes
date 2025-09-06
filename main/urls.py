from django.urls import path
from . import views

urlpatterns = [
    path("", views.random_quote, name="random_quote"),
    path("like/<int:id>/", views.like_quote, name="like_quote"),
    path("dislike/<int:id>/", views.dislike_quote, name="dislike_quote"),
    path("top/", views.top_quotes, name="top_quotes"),
]
