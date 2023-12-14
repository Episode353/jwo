from django.shortcuts import render, HttpResponse
from .models import account, foodreview


# Create your views here.
def home(request):
    seep_coin_list = account.objects.all().order_by('-coin_count')
    return render(request, "home.html", {'seep_coin_list': seep_coin_list})

def seepcoin(request):
    seep_coin_list = account.objects.all().order_by('-coin_count')
    return render(request, "seepcoin.html", {'seep_coin_list': seep_coin_list})
    
def board(request):
    return render(request, "board.html")

def blog(request):
    return render(request, "blog.html")
    
def foodreviewpage(request):
    food_review_list = foodreview.objects.all().order_by('reviewDate')
    return render(request, "foodreview.html", {'food_review_list': food_review_list})
