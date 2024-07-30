from django.shortcuts import render, redirect
from worm.models import Worm
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.utils import timezone

def main(request):
    # Fetch the first worm that is alive
    living_worm = Worm.objects.filter(is_alive=True).first()

    if living_worm:
        # Calculate the Current Sleep, Hunger, and Happiness
        
        # Current time
        now = timezone.localtime(timezone.now())

        # Calculate hours since last slept
        if living_worm.last_slept:
            hours_since_slept = (now - living_worm.last_slept).total_seconds() // 3600
            living_worm.sleep = max(0, 10 - int(hours_since_slept))
        
        # Calculate hours since last fed
        if living_worm.last_fed:
            hours_since_fed = (now - living_worm.last_fed).total_seconds() // 3600
            living_worm.hunger = max(0, 10 - int(hours_since_fed))
        
        # Calculate hours since last played
        if living_worm.last_played:
            hours_since_played = (now - living_worm.last_played).total_seconds() // 3600
            living_worm.happiness = max(0, 10 - int(hours_since_played))
        
        # Calculate the Current Health
        living_worm.health = round((living_worm.sleep + living_worm.hunger + living_worm.happiness) / 3)

        # Subtract the revives from the health
        # If a worm is revived zero times, were subtracting zero and it can go up to full health
        # If a worm is revived two times, were subtracting two and it can only go up to eight health.
        living_worm.health -= living_worm.times_revived

        # Ensure health is at least 0 to avoid integrity errors
        living_worm.health = max(0, living_worm.health)

        # If the health <= 0, set is_alive to False and record time of death
        if living_worm.health <= 0 and living_worm.is_alive:
            living_worm.is_alive = False
            living_worm.time_of_death = now

        # Calculate the worm's age and update the badge
        worm_age_days = (now - living_worm.created_at).days

        if 0 <= worm_age_days <= 6:
            living_worm.badge = 1
        elif 7 <= worm_age_days <= 13:
            living_worm.badge = 2
        elif 14 <= worm_age_days <= 20:
            living_worm.badge = 3
        elif 21 <= worm_age_days <= 29:
            living_worm.badge = 4
        elif 30 <= worm_age_days <= 59:
            living_worm.badge = 5
        elif 60 <= worm_age_days <= 89:
            living_worm.badge = 6
        elif 90 <= worm_age_days <= 119:
            living_worm.badge = 7
        elif 120 <= worm_age_days <= 149:
            living_worm.badge = 8
        elif 150 <= worm_age_days <= 179:
            living_worm.badge = 9
        else:  # 180 and above
            living_worm.badge = 10
        
        # Save the updated worm
        living_worm.save()


    # Pass the living_worm to the template
    return render(request, 'worm_main.html', {'living_worm': living_worm})


from django.shortcuts import render, redirect
from worm.models import Worm
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

#@csrf_exempt  # You may enable for debugging
def create_worm(request):
    if request.method == 'POST':
        # Check if there are any worms alive
        alive_worms_exist = Worm.objects.filter(is_alive=True).exists()
        if alive_worms_exist:
            # If alive worms exist, redirect to the main page with a message
            return custom_404_view(request, "There are already worms alive. You can't create a new worm until all are dead.")
        
        name = request.POST.get('name')
        if name:
            # Capitalize the first letter and make the rest lowercase
            formatted_name = name.capitalize()
            
            # Check if the name matches any dead worms
            if Worm.objects.filter(name=formatted_name, is_alive=False).exists():
                return custom_404_view(request, "A worm with this name has already exists. Please choose a different name.")
            
            # Get the current time
            now = timezone.localtime(timezone.now())
            
            # Create the worm with the current time for sleep, fed, and played times
            Worm.objects.create(
                name=formatted_name,
                last_slept=now,
                last_fed=now,
                last_played=now
            )
            return redirect('worm/main')
    
    # In case of GET request or no name provided, redirect to main page
    return redirect('worm/main')


from django.shortcuts import render, redirect
from worm.models import Worm
from django.utils import timezone

def worm_feed(request):
    worm = Worm.objects.filter(is_alive=True).first()
    if worm:
        worm.last_fed = timezone.localtime(timezone.now())
        worm.save()
    return redirect('worm/main')

def worm_play(request):
    worm = Worm.objects.filter(is_alive=True).first()
    if worm:
        worm.last_played = timezone.localtime(timezone.now())
        worm.save()
    return redirect('worm/main')

def worm_sleep(request):
    worm = Worm.objects.filter(is_alive=True).first()
    if worm:
        worm.last_slept = timezone.localtime(timezone.now())
        worm.save()
    return redirect('worm/main')


def graveyard(request):
    dead_worms = Worm.objects.filter(is_alive=False)
    return render(request, 'graveyard.html', {'dead_worms': dead_worms})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Worm
from myapp.models import Profile, SeepCoinTransaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from myapp.views import custom_404_view


def revive(request, worm_name):
    if not request.user.is_authenticated:
        return custom_404_view(request, "You need to be logged in and have at least one seep coin to revive a worm.")
    user_profile = request.user.profile
    joe = User.objects.get(username='joe')
    
    # Check if there are no worms currently alive
    if not Worm.objects.filter(is_alive=True).exists():


        # Check if the user has more than 0 SeepCoins
        if user_profile.coin_count > 0:
            worm = get_object_or_404(Worm, name=worm_name, is_alive=False)
            
            # Check if the worm has not exceed 9 revives
            if worm.times_revived >= 9:
                return custom_404_view(request, "This worm been revived too many times.")

            # Revive the worm
            worm.is_alive = True
            worm.last_slept = timezone.localtime(timezone.now())
            worm.last_played = timezone.localtime(timezone.now())
            worm.last_fed = timezone.localtime(timezone.now())

            worm.times_revived += 1

            worm.save()
            
            # Deduct one SeepCoin from the user and send it to Joe
            user_profile.coin_count -= 1
            user_profile.save()
            
            joe.profile.coin_count += 1
            joe.profile.save()
            
            # Create a SeepCoinTransaction
            SeepCoinTransaction.objects.create(sender=request.user, receiver=joe, amount=1)
            
            # Redirect to the main page or any other page you prefer
            return redirect('worm/main')
        
        # If the user doesn't have enough SeepCoins, return a custom 404 error with a message
        return custom_404_view(request, "You don't have enough SeepCoins to revive the worm.")
    
    # If there are worms currently alive, return a custom 404 error with a message
    return custom_404_view(request, "You cannot revive a worm while there are worms currently alive.")

# Rest of your views.py remains unchanged
