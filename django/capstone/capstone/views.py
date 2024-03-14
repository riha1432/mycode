from django.http import HttpResponse


def claude(request):
    return HttpResponse("Hello, world. You're at the polls index.")