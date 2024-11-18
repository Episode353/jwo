from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Frontend view for the button
def button_frontend(request):
    if request.user.is_authenticated:
        current_user = request.user.username  # Get logged-in user's username
    else:
        current_user = 'Guest'  # Show 'Guest' if the user is not logged in

    # Check if user is logged in
    if not request.user.is_authenticated:
        message = "You must be logged in to interact with the button"
        return custom_404_view(request, message)

    return render(request, 'button_frontend.html', {'current_user': current_user})

# Backend view for button press and clearing updates
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
from .models import ButtonUpdate


=======
from .models import Update

# Backend view for button press and saving updates to the model
>>>>>>> 198f3908512779f0f3c28f02e201c9642d9a8ce5
@csrf_exempt
def button_backend(request):
    if request.method == 'POST':
        current_user = request.user if request.user.is_authenticated else None
        message = f"Button pressed by: {current_user.username if current_user else 'Guest'}"
<<<<<<< HEAD

        # Debugging print statement
        print(f"Button Pressed: {message}")

        # Save the update to the database
        ButtonUpdate.objects.create(user=current_user, message=message)

        # Return the updated list of button press updates as a JSON response
        updates = ButtonUpdate.objects.all().order_by('-timestamp')  # You can adjust ordering if needed
        updates_list = [{'user': update.user.username if update.user else 'Guest', 'message': update.message, 'timestamp': update.timestamp} for update in updates]
        print(f"Updates: {updates_list}")  # Debugging print for updates

        return JsonResponse({'updates': updates_list})

    return render(request, 'button_backend.html')


=======
        
        # Save the update to the database
        Update.objects.create(user=current_user, message=message)

        # Retrieve the latest updates from the database
        updates = Update.objects.all().order_by('-timestamp')

        # Prepare updates for JSON response
        updates_data = [f"{update.user.username if update.user else 'Guest'}: {update.message}" for update in updates]
        
        return JsonResponse({'updates': updates_data})

    return render(request, 'button_backend.html')
>>>>>>> 198f3908512779f0f3c28f02e201c9642d9a8ce5


# View to clear updates when the "Clear" button is pressed


@csrf_exempt
def clear_updates(request):
    if request.method == 'POST':
<<<<<<< HEAD
        ButtonUpdate.objects.all().delete()
=======
        Update.objects.all().delete()  # Delete all updates
>>>>>>> 198f3908512779f0f3c28f02e201c9642d9a8ce5
        return JsonResponse({'updates': []})

    return JsonResponse({'error': 'Invalid request'}, status=400)



# Custom 404 view for displaying error messages
def custom_404_view(request, message):
    return render(request, '404.html', {'message': message})


def get_updates(request):
<<<<<<< HEAD
    updates = ButtonUpdate.objects.all().order_by('-timestamp')
    print(updates)
    updates_list = [{'user': update.user.username if update.user else 'Guest', 'message': update.message, 'timestamp': update.timestamp} for update in updates]
    return JsonResponse({'updates': updates_list})
=======
    updates = Update.objects.all().order_by('-timestamp')
    updates_data = [f"{update.user.username if update.user else 'Guest'}: {update.message}" for update in updates]
    return JsonResponse({'updates': updates_data})


>>>>>>> 198f3908512779f0f3c28f02e201c9642d9a8ce5
