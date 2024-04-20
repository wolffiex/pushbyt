from django.urls import path
from main.views import get_preview, get_player

urlpatterns = [
    path("v1/preview.webp", get_preview, name="get_preview"),
    path("player/<str:name>", get_player, name="get_player"),
]
