from django.shortcuts import render

from search_engine.main import engine


def index(request):
    if request.method == 'GET':
        return render(request, 'main/webInterface.html')
    if request.method == 'POST':
        query = request.POST.get("query", "")
        a = engine.search(query)
        context = {
            'query': a,
        }
        return render(request, 'main/results.html', context)
    return render(request, 'main/webInterface.html')
