from django.shortcuts import render


def hello_world(request):
    return render(request, 'index.html', {'greeting': 'Hello, world!'})
