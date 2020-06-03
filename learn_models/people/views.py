from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'index.html')
def add(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    return HttpResponse(str(int(a)+int(b)))
