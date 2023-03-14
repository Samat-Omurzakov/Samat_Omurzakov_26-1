from django.shortcuts import HttpResponse
from datetime import datetime

def hello_view(request):
    if request.method == 'GET':
        return HttpResponse("Hello! Its my project")

def now_date_view(request):
    if request.method == 'GET':
        now_date = datetime.now()
        return HttpResponse(f"{now_date}")

def goodbye_view(request):
    if request.method == 'GET':
        return HttpResponse("Goodbye user!")