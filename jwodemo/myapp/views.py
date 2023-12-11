from django.shortcuts import render, HttpResponse
from .models import account


# Create your views here.
def home(request):
    return render(request, "home.html")

def seepcoin(request):
    seep_coin_list = account.objects.all().order_by('-coin_count')
    return render(request, "seepcoin.html", {'seep_coin_list': seep_coin_list})
    
def board(request):
    return render(request, "board.html")

def blog(request):
    return render(request, "blog.html")
    
def foodreview(request):
    return render(request, "foodreview.html")