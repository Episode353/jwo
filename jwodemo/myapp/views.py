from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime
from .models import Profile
from .models import foodreview, SeepCoinTransaction, todo
from django.conf import settings



BASE_DIR = settings.BASE_DIR
from .forms import CoinMessageForm
import os
import random
import time

def home(request):
    seep_coin_list = User.objects.filter(profile__coin_count__gt=0).order_by('-profile__coin_count')[:3]
    users = User.objects.exclude(pk=request.user.id).filter(profile__coin_count__gt=0).order_by('-profile__coin_count')[:3]


    # Logic for randomizing and selecting a file
    shuffle_page = request.GET.get('shuffle')
    if shuffle_page:
        # Load the specified page indicated by the shuffle parameter
        template_name = f"static/html-shuffle/{shuffle_page}"
        if not os.path.exists(os.path.join('myapp', template_name)):
            print(f"SHUFFLE_FILE DOES NOT EXIST: ", shuffle_page)
            # Display an error message when the file does not exist
            template_name = "static/html-shuffle/error.html"
    else:
        # List all files in the 'html-shuffle' directory excluding "error.html"
        shuffle_files = [file for file in os.listdir(os.path.join(settings.BASE_DIR, 'myapp', 'static', 'html-shuffle')) if file != 'error.html']

        # Pick a random file
        random_file = random.choice(shuffle_files)
        template_name = f"static/html-shuffle/{random_file}"
        print(f"SHUFFLE_FILE: ", template_name)

    # Get the current timestamp including the hour
    current_timestamp = int(datetime.now().timestamp())

    return render(request, "home.html", {'seep_coin_list': seep_coin_list, 'users': users, 'template_name': template_name, 'current_timestamp': current_timestamp})




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


def get_drawings(request):
    drawings_folder = os.path.join('jwo/jwodemo/media/drawings')
    os.makedirs(drawings_folder, exist_ok=True)
    drawings = [filename for filename in os.listdir(drawings_folder) if filename.endswith('.png')]
    return JsonResponse({'drawings': drawings})

@csrf_exempt
def save_drawing(request):
    if request.method == 'POST':
        try:
            # Get the image data from the form data
            image_data = request.POST.get('imageData', '').replace('data:image/png;base64,', '')

            # Decode the base64 image data
            decoded_image_data = base64.b64decode(image_data)

            # Create a unique filename
            filename = f'board_drawing_no_{int(time.time())}.png'
            filepath = os.path.join('jwo/jwodemo/media/drawings', filename)

            # Create the 'media/drawings' directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # Save the image to the media folder
            with open(filepath, 'wb') as f:
                f.write(decoded_image_data)

            return JsonResponse({'success': True, 'filename': filename})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


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
    # Exclude users with zero seep coins
    seep_coin_list = User.objects.exclude(profile__coin_count=0).order_by('-profile__coin_count')



    # Exclude the logged-in user
    users = User.objects.exclude(pk=request.user.id)

    print(users)  # Add this line to check the users in the console
    return render(request, "seepcoin.html", {'seep_coin_list': seep_coin_list, 'users': users})



def board(request):
    return render(request, "board.html")

def gallery(request):
    return render(request, "gallery.html")


def blog(request):
    return render(request, "blog.html")

def tool(request):
    return render(request, "tool.html")

def foodpage(request):
    food_review_list = foodreview.objects.all().order_by('-Date')
    return render(request, "foodreview.html", {'food_review_list': food_review_list})

def food_ar(request, slug):
    food_review = foodreview.objects.get(slug=slug)
    html_file_path = os.path.join('jwo/jwodemo/static/food-review-posts/', food_review.slug +  '.html')
    print(html_file_path)

    try:
        with open(html_file_path, 'r', encoding='utf-8-sig') as html_file:  # Use 'utf-8-sig' to handle BOM
            html_content = html_file.read()
    except FileNotFoundError:
        # Handle file not found error
        html_content = None

    return render(request, "food_template.html", {'food_review': food_review, 'html_content': html_content})


def translator(request):
    return render(request, "translator.html")

def mapdirect(request):
    return redirect("http://c-municipality.gl.at.ply.gg:45118/")


def todo_view(request):  # Renamed to avoid conflict with model name
    todo_list = todo.objects.all().order_by('position')
    return render(request, "todo.html", {'todo_list': todo_list})

