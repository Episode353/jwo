from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "home.html")

def seepcoin(request):
    return render(request, "seepcoin.html")
    
def board(request):
    return render(request, "board.html")

def blog(request):
    return render(request, "blog.html")
    
def foodreview(request):
    return render(request, "foodreview.html")