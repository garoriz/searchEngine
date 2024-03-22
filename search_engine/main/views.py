from django.shortcuts import render

from . import engine


def index(request):
    if request.method == 'GET':
        return render(request, 'main/webInterface.html')
    if request.method == 'POST':
        query = request.POST.get("query", "")
        result = engine.search(query)
        if len(result) == 0:
            return render(request, 'main/no_results.html')
        url1 = result[0][0]
        url2 = result[1][0]
        url3 = result[2][0]
        url4 = result[3][0]
        url5 = result[4][0]
        url6 = result[5][0]
        url7 = result[6][0]
        url8 = result[7][0]
        url9 = result[8][0]
        url10 = result[9][0]
        context = {
            'url1': url1,
            'url2': url2,
            'url3': url3,
            'url4': url4,
            'url5': url5,
            'url6': url6,
            'url7': url7,
            'url8': url8,
            'url9': url9,
            'url10': url10,
        }
        return render(request, 'main/results.html', context)
    return render(request, 'main/webInterface.html')
