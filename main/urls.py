from django.urls import path
from main.views import get_webp, get_player

urlpatterns = [
    path("anim/<str:name>", get_webp, name="get_webp"),
    path("player/<str:name>", get_player, name="get_player"),
]
