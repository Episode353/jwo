from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Stock, StockHistory
import numpy as np
import json
from datetime import timedelta

import random

from decimal import Decimal
import numpy as np
from django.utils import timezone
from datetime import timedelta
from .models import Stock, StockHistory

from decimal import Decimal
import numpy as np
from django.utils import timezone
from datetime import timedelta
from .models import Stock, StockHistory
from django.utils import timezone
from .models import Stock, StockHistory
from decimal import Decimal
from datetime import timedelta
import numpy as np

def update_stock(stock, history_days=30):
    now = timezone.now()
    interval = timedelta(days=1)  # Assume we want to update every day

    # Ensure stock value isn't too small
    stock.value = max(stock.value, Decimal('0.1'))

    # Get the last updated timestamp, or if no history exists, use stock's last_updated
    last_history = stock.history.last()
    if last_history:
        last_timestamp = last_history.timestamp
    else:
        last_timestamp = stock.last_updated if stock.last_updated else now - timedelta(days=1)
        # Initialize the first entry if no history exists
        StockHistory.objects.create(stock=stock, price=stock.value, timestamp=last_timestamp)

    updated = False  # Flag to track if the stock value has been updated

    # Only proceed if enough time has passed
    while now > last_timestamp + interval:
        last_timestamp += interval

        # Randomize the stock price within ±1.00 to ensure smaller changes
        change = Decimal(np.random.uniform(-1, 1)).quantize(Decimal('0.01'))
        new_price = Decimal(stock.value) + change

        # Ensure the new price does not go below 0.1
        new_price = max(new_price, Decimal('0.1'))

        # Record the stock's updated value in history
        StockHistory.objects.create(stock=stock, price=new_price, timestamp=last_timestamp)

        # Update the stock value to the new price
        stock.value = new_price
        updated = True  # Indicate that the stock value was updated

    # If the stock value was updated, also update the stock's last_updated field and record the current value
    if updated:
        stock.last_updated = now
        stock.save()
        StockHistory.objects.create(stock=stock, price=stock.value, timestamp=now)

    # Clean up old history records
    cutoff_date = now - timedelta(days=history_days)
    StockHistory.objects.filter(stock=stock, timestamp__lt=cutoff_date).delete()



def stock_home(request):
    # Sort stocks by price in descending order
    stocks = Stock.objects.all().order_by('-value')

    for stock in stocks:
        update_stock(stock)

    stock_data_json = json.dumps({
        stock.name: {
            'color': stock.color,
            'data': list(stock.history.values('timestamp', 'price'))
        }
        for stock in stocks
    }, default=str)

    context = {
        'stocks': stocks,
        'stock_data': stock_data_json,
    }

    if request.user.is_authenticated:
        # Check if the user has created a stock
        user_has_created_stock = Stock.objects.filter(created_by=request.user).exists()
        context['user_has_created_stock'] = user_has_created_stock

    return render(request, 'stocks.html', context)




from django.shortcuts import get_object_or_404
from .models import Stock

from django.shortcuts import render, get_object_or_404
from .models import Stock, StockOwnership

def stock_detail(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)

    # Check if the logged-in user is the creator
    is_creator = False
    user_ownership = None  # Initialize ownership variable to None
    ownerships = StockOwnership.objects.filter(stock=stock)  # Fetch all ownership records for this stock

    if request.user.is_authenticated:
        is_creator = (request.user == stock.created_by)

        # Check if the logged-in user owns any of this stock
        user_ownership = ownerships.filter(user=request.user).first()  # Get the first ownership record if it exists

    stock_data_json = json.dumps({
        'color': stock.color,
        'data': list(stock.history.values('timestamp', 'price'))
    }, default=str)

    context = {
        'stock': stock,
        'stock_data': stock_data_json,
        'is_creator': is_creator,  # Pass 'is_creator' to template
        'ownership': user_ownership,  # Pass logged-in user's ownership to template
        'ownerships': ownerships,     # Pass all ownerships to template
    }

    return render(request, 'stock_detail.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StockCreateForm

@login_required
def create_stock(request):
    if request.method == 'POST':
        form = StockCreateForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.created_by = request.user  # Assign the logged-in user to created_by
            stock.save()  # Save the stock

            # Create the ownership record
            StockOwnership.objects.create(user=request.user, stock=stock, quantity=0)

            return redirect('stock_home')  # Redirect to stock home or another appropriate page
    else:
        form = StockCreateForm()

    return render(request, 'create_stock.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditStockForm
from .models import Stock, StockOwnership

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Stock, StockOwnership
from .forms import EditStockForm

@login_required
def edit_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)

    # Check if the current user owns this stock
    if not StockOwnership.objects.filter(user=request.user, stock=stock).exists():
        # Redirect if the user doesn't own the stock
        return redirect('stock_home')

    if request.method == 'POST':
        form = EditStockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock_detail', stock_id=stock_id)
    else:
        form = EditStockForm(instance=stock)

    context = {
        'form': form,
        'stock': stock
    }

    return render(request, 'edit_stock.html', context)



from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, StockOwnership
from myapp.models import Profile
from decimal import Decimal


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, StockOwnership
from myapp.models import Profile
from decimal import Decimal, ROUND_DOWN

@login_required
def buy_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    user_profile = request.user.profile

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))

        if quantity <= 0:
            messages.error(request, 'You must specify a quantity greater than zero.')
            return redirect('stock_detail', stock_id=stock_id)

        stock_value = Decimal(stock.value)
        total_cost = stock_value * Decimal(quantity)

        if Decimal(user_profile.coin_count).quantize(Decimal('0.01'), rounding=ROUND_DOWN) < total_cost:
            messages.error(request, 'You do not have enough Seep Coins to make this purchase.')
            return redirect('stock_detail', stock_id=stock_id)

        user_profile.coin_count = Decimal(user_profile.coin_count).quantize(Decimal('0.01'), rounding=ROUND_DOWN) - total_cost
        user_profile.save()

        ownership, created = StockOwnership.objects.get_or_create(user=request.user, stock=stock)
        ownership.quantity += quantity
        ownership.save()

        messages.success(request, f'You have successfully purchased {quantity} units of {stock.name}.')
        return redirect('stock_detail', stock_id=stock_id)

@login_required
def sell_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    user_profile = request.user.profile

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))

        if quantity <= 0:
            messages.error(request, 'You must specify a quantity greater than zero.')
            return redirect('stock_detail', stock_id=stock_id)

        try:
            ownership = StockOwnership.objects.get(user=request.user, stock=stock)
        except StockOwnership.DoesNotExist:
            messages.error(request, 'You do not own any of this stock to sell.')
            return redirect('stock_detail', stock_id=stock_id)

        if ownership.quantity < quantity:
            messages.error(request, 'You do not own enough of this stock to sell.')
            return redirect('stock_detail', stock_id=stock_id)

        stock_value = Decimal(stock.value)
        total_earnings = stock_value * Decimal(quantity)

        ownership.quantity -= quantity
        ownership.save()

        if ownership.quantity == 0:
            ownership.delete()

        user_profile.coin_count = Decimal(user_profile.coin_count).quantize(Decimal('0.01'), rounding=ROUND_DOWN) + total_earnings
        user_profile.save()

        messages.success(request, f'You have successfully sold {quantity} units of {stock.name}.')
        return redirect('stock_detail', stock_id=stock_id)
