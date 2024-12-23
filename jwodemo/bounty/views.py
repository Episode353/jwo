from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Bounty

def bounty_list(request):
    tiers = {
        'I': Bounty.objects.filter(tier='I', completed=False),
        'II': Bounty.objects.filter(tier='II', completed=False),
        'III': Bounty.objects.filter(tier='III', completed=False),
        'IV': Bounty.objects.filter(tier='IV', completed=False),
        'V': Bounty.objects.filter(tier='V', completed=False),
    }
    return render(request, 'bounties.html', {'tiers': tiers})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bounty
from .forms import BountyForm

@login_required
def create_bounty(request):
    if request.method == 'POST':
        form = BountyForm(request.POST)
        if form.is_valid():
            bounty = form.save(commit=False)
            bounty.creator = request.user  # Associate logged-in user
            bounty.save()
            return redirect('bounty_list')
    else:
        form = BountyForm()
    return render(request, 'create_bounty.html', {'form': form})

@login_required
def edit_bounty(request, bounty_id):
    bounty = get_object_or_404(Bounty, id=bounty_id, creator=request.user)
    if request.method == 'POST':
        form = BountyForm(request.POST, instance=bounty)
        if form.is_valid():
            form.save()
            return redirect('bounty_list')
    else:
        form = BountyForm(instance=bounty)
    return render(request, 'edit_bounty.html', {'form': form, 'bounty': bounty})

@login_required
def delete_bounty(request, bounty_id):
    bounty = get_object_or_404(Bounty, id=bounty_id, creator=request.user)
    if request.method == 'POST':
        bounty.delete()
        return redirect('bounty_list')
    return render(request, 'delete_bounty.html', {'bounty': bounty})
