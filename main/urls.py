from django.urls import path
from main.views import get_webp

urlpatterns = [
    path("anim/<str:name>", get_webp, name="get_webp"),
]
