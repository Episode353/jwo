from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Profile
from .models import foodreview, SeepCoinTransaction
from .forms import CoinMessageForm 
import os
import random
import time

# Create your views here.
def home(request):
    seep_coin_list = User.objects.all().order_by('-profile__coin_count')
    users = User.objects.exclude(pk=request.user.id)

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

    return render(request, "home.html", {'seep_coin_list': seep_coin_list, 'users': users, 'template_name': template_name,})

@login_required
def edit_coin_message(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        # Get the user instance
        user = get_object_or_404(User, pk=user_id)

        # Check if the user making the request is the owner of the profile
        if request.user == user:
            form = CoinMessageForm(request.POST)  # Create an instance of the form with the POST data

            if form.is_valid():  # Check if the form is valid
                coin_message = form.cleaned_data['coin_message']
                user.profile.coin_message = coin_message
                user.profile.save()
            else:
                # Display a success message including the maximum length
                max_length = form.fields['coin_message'].max_length
                messages.success(request, f"Max length is {max_length} charachters")

    return redirect('seepcoin')

@login_required
def trade_seep_coins(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        amount = int(request.POST.get('amount', 0))

        # Check if the sender has enough coins
        if amount > 0 and amount <= request.user.profile.coin_count:
            receiver = User.objects.get(pk=receiver_id)

            # Create a new SeepCoinTransaction
            SeepCoinTransaction.objects.create(sender=request.user, receiver=receiver, amount=amount)

            # Update sender and receiver coin counts
            request.user.profile.coin_count -= amount
            request.user.profile.save()

            receiver.profile.coin_count += amount
            receiver.profile.save()

    return redirect('seepcoin')

def seepcoin(request):
    seep_coin_list = User.objects.all().order_by('-profile__coin_count')
    users = User.objects.exclude(pk=request.user.id)
    print(users)  # Add this line to check the users in the console
    return render(request, "seepcoin.html", {'seep_coin_list': seep_coin_list, 'users': users})

    
def board(request):
    return render(request, "board.html")

def blog(request):
    return render(request, "blog.html")
    
def foodpage(request):
    food_review_list = foodreview.objects.all().order_by('Date')
    return render(request, "foodreview.html", {'food_review_list': food_review_list})

def food_ar(request, slug):
    food_review = foodreview.objects.get(slug=slug)
    html_file_path = os.path.join('myapp', 'static', 'food-review-posts', food_review.slug +  '.html')
    print(html_file_path)

    try:
        with open(html_file_path, 'r', encoding='utf-8-sig') as html_file:  # Use 'utf-8-sig' to handle BOM
            html_content = html_file.read()
    except FileNotFoundError:
        # Handle file not found error
        html_content = None

    return render(request, "food_template.html", {'food_review': food_review, 'html_content': html_content})