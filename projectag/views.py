from django.shortcuts import render
from django.http import JsonResponse

def ping_view(request):
    return JsonResponse({"status": "success", "message": "pong"})
