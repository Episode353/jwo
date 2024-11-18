from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Global variable to store updates
updates = []

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
from .models import Update

# Backend view for button press and saving updates to the model
@csrf_exempt
def button_backend(request):
    if request.method == 'POST':
        current_user = request.user if request.user.is_authenticated else None
        message = f"Button pressed by: {current_user.username if current_user else 'Guest'}"
        
        # Save the update to the database
        Update.objects.create(user=current_user, message=message)

        # Retrieve the latest updates from the database
        updates = Update.objects.all().order_by('-timestamp')

        # Prepare updates for JSON response
        updates_data = [f"{update.user.username if update.user else 'Guest'}: {update.message}" for update in updates]
        
        return JsonResponse({'updates': updates_data})

    return render(request, 'button_backend.html')


# View to clear updates when the "Clear" button is pressed


@csrf_exempt
def clear_updates(request):
    if request.method == 'POST':
        Update.objects.all().delete()  # Delete all updates
        return JsonResponse({'updates': []})

    return JsonResponse({'error': 'Invalid request'}, status=400)



# Custom 404 view for displaying error messages
def custom_404_view(request, message):
    return render(request, '404.html', {'message': message})


def get_updates(request):
    updates = Update.objects.all().order_by('-timestamp')
    updates_data = [f"{update.user.username if update.user else 'Guest'}: {update.message}" for update in updates]
    return JsonResponse({'updates': updates_data})


