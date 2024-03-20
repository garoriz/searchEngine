from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'main/webInterface.html')


def postquery(request):
    name = request.POST.get("query", "")
    return HttpResponse(f"<h2>Query: {name}</h2>")
