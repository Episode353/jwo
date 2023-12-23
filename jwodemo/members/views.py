from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, "There was an error logging in, try again....")
            return redirect('login')


    else:
        return render(request, 'authenticate/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged out.")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register_user.html', {
        'form': form,
    })

@login_required
def account(request):
    profile = request.user.profile
    return render(request, "account.html", {'profile': profile})

@login_required
def edit_profile(request):
    if request.method == "POST":
        new_name = request.POST.get('name')
        request.user.profile.name = new_name
        request.user.profile.save()
        return redirect('account')

    return render(request, 'edit_profile.html')

def coin_coint(request):
    return render(request, "coin_count.html")