from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from functools import wraps
from django.contrib.auth.mixins import LoginRequiredMixin
from myapp.models import Profile
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.urls import reverse
from .forms import EditProfileForm, PasswordChangingForm

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
    messages.success(request, "You have been logged out.")
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

def login_required_with_message(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.success(request, "You must be logged in to view this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from stock.models import StockOwnership
@login_required_with_message
def account(request):
    profile = request.user.profile
    # Fetch stocks owned by the user
    owned_stocks = StockOwnership.objects.filter(user=request.user)
    return render(request, "account.html", {
        'profile': profile,
        'owned_stocks': owned_stocks,
    })


@login_required_with_message
def edit_profile(request):
    if request.method == "POST":
        new_name = request.POST.get('name')
        request.user.profile.name = new_name
        request.user.profile.save()
        return redirect('account')
    return render(request, 'edit_profile.html')


class EditProfilePageView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'steam_url', 'twitter_url', 'instagram_url', 'discord_url']

    def get_form(self, form_class=None):
        form = super(EditProfilePageView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form

    def get_success_url(self):
        return reverse('show_profile_page', kwargs={'pk': self.object.pk})


from stock.models import StockOwnership

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        # Get the profile user being viewed
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        # Fetch the stocks owned by the profile user
        owned_stocks = StockOwnership.objects.filter(user=page_user.user)

        context["page_user"] = page_user
        context["owned_stocks"] = owned_stocks
        return context





class UserEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('bloghome')

    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    # success_url = reverse_lazy('home')

def password_success(request):
    return render(request, 'registration/password_success.html', {})