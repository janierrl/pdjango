from django.shortcuts import render

def handler404(request, exception):
    return render(request, 'errors/404.html')

def handler500(request):
    return render(request, 'errors/500.html')