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
@csrf_exempt
def button_backend(request):
    global updates

    if request.method == 'POST':
        current_user = request.user.username if request.user.is_authenticated else 'Guest'
        updates.append(f"Button pressed by: {current_user}")

        # Return the updated list of button press updates as a JSON response
        return JsonResponse({'updates': updates})

    # Render the backend page
    return render(request, 'button_backend.html', {'updates': updates})

# View to clear updates when the "Clear" button is pressed

@csrf_exempt
def clear_updates(request):
    global updates

    if request.method == 'POST':
        updates.clear()
        return JsonResponse({'updates': updates})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# Custom 404 view for displaying error messages
def custom_404_view(request, message):
    return render(request, '404.html', {'message': message})


# View to get updates for the frontend and backend
def get_updates(request):
    return JsonResponse({'updates': updates})



# Custom 404 view for displaying error messages
def custom_404_view(request, message):
    return render(request, '404.html', {'message': message})
