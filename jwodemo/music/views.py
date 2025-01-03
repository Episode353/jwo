from django.shortcuts import render, redirect
from .models import Album

def music_items(request):
    music_review_list = Album.objects.all()
    return render(request, "music_items.html", {'music_review_list': music_review_list})

def album(request, slug):
    album_review = Album.objects.get(slug=slug)
    return render(request, "music_review.html", {'album_review': album_review})
from django.shortcuts import render, redirect
from .models import Album, Recommendation
from django.contrib import messages
from django.utils import timezone

def submit_recommendation(request):
    if request.method == 'POST':
        recommendation_text = request.POST.get('recommendation').strip()  # Remove leading/trailing whitespace
        if recommendation_text:  # Check if recommendation text is not empty
            browser_info = request.headers.get('User-Agent', 'Unknown Browser')
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S %Z")
            if request.user.is_authenticated:
                user_name = request.user.username
                recommendation_text += ' | User: ' + user_name
            recommendation_text += ' | Timestamp: ' + timestamp
            # Include location if available
            location = request.headers.get('X-AppEngine-Country', 'Unknown Location')
            recommendation_text += ' | Location: ' + location
            recommendation_text += ' | Browser: ' + browser_info
            Recommendation.objects.create(recommendation_text=recommendation_text)
            messages.success(request, 'Your recommendation has been sent successfully!')
        else:
            messages.error(request, 'Empty recommendation!')
        return redirect('music')
    else:
        return redirect('music')  # Redirect if not a POST request
