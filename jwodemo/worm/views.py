from django.shortcuts import render, redirect
from worm.models import Worm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def main(request):
    # Fetch the first worm that is alive
    living_worm = Worm.objects.filter(is_alive=True).first()
    # Pass the living_worm to the template

    

    return render(request, "worm_main.html", {'living_worm': living_worm})

@csrf_exempt  # Temporary, use with caution in production.
def create_worm(request):
    if request.method == 'POST':
        # Check if there are any worms alive
        alive_worms_exist = Worm.objects.filter(is_alive=True).exists()
        if alive_worms_exist:
            # If alive worms exist, redirect to the main page with a message
            return HttpResponse("There are already worms alive. You can't create a new worm until all are dead.", status=403)
        
        name = request.POST.get('name')
        if name:
            Worm.objects.create(name=name)
            return redirect('worm/main')
    
    # In case of GET request or no name provided, redirect to main page
    return redirect('worm/main')
