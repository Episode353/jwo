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
from .models import ButtonUpdate


@csrf_exempt
def button_backend(request):
    if request.method == 'POST':
        current_user = request.user if request.user.is_authenticated else None
        message = f"Button pressed by: {current_user.username if current_user else 'Guest'}"

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




# View to clear updates when the "Clear" button is pressed

@csrf_exempt
def clear_updates(request):
    if request.method == 'POST':
        ButtonUpdate.objects.all().delete()
        return JsonResponse({'updates': []})

    return JsonResponse({'error': 'Invalid request'}, status=400)



# Custom 404 view for displaying error messages
def custom_404_view(request, message):
    return render(request, '404.html', {'message': message})


# View to get updates for the frontend and backend
def get_updates(request):
    updates = ButtonUpdate.objects.all().order_by('-timestamp')
    print(updates)
    updates_list = [{'user': update.user.username if update.user else 'Guest', 'message': update.message, 'timestamp': update.timestamp} for update in updates]
    return JsonResponse({'updates': updates_list})
