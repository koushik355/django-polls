from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def blogs(request):
    return JsonResponse('hello', safe=False)
