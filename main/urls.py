from django.urls import path
from main.views import get_preview, generate, get_render, get_simulator

urlpatterns = [
    path("v1/preview.webp", get_preview, name="get_preview"),
    path("command/generate", generate, name="generate"),
    path("simulator", get_simulator, name="simulator"),
    path("render/<str:file_name>", get_render, name="get_render"),
]
