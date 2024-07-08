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
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone

#@csrf_exempt  # You may enable for debugging
def create_worm(request):
    if request.method == 'POST':
        # Check if there are any worms alive
        alive_worms_exist = Worm.objects.filter(is_alive=True).exists()
        if alive_worms_exist:
            # If alive worms exist, redirect to the main page with a message
            return HttpResponse("There are already worms alive. You can't create a new worm until all are dead.", status=403)
        
        name = request.POST.get('name')
        if name:
            # Capitalize the first letter and make the rest lowercase
            formatted_name = name.capitalize()
            
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