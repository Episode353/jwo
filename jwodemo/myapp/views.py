from django.shortcuts import render, HttpResponse
from .models import account, foodreview
import os
import random
import time

# Create your views here.
def home(request):
    seep_coin_list = account.objects.all().order_by('-coin_count')

    # Logic for randomizing and selecting a file
    shuffle_page = request.GET.get('shuffle')
    if shuffle_page:
        # Load the specified page indicated by the shuffle parameter
        template_name = f"static/html-shuffle/{shuffle_page}"
        if not os.path.exists(os.path.join('myapp', template_name)):
            # Display an error message when the file does not exist
            template_name = "static/html-shuffle/error.html"
    else:
        # Use the current time in milliseconds as a seed for the random number generator
        seed = int(time.time() * 1000)
        random.seed(seed)

        # List all files in the 'html-shuffle' directory
        shuffle_files = os.listdir(os.path.join('myapp', 'static', 'html-shuffle'))

        # Pick a random file
        random_file = random.choice(shuffle_files)
        template_name = f"static/html-shuffle/{random_file}"

    return render(request, "home.html", {'seep_coin_list': seep_coin_list, 'template_name': template_name})


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
