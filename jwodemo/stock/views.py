from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Stock, StockHistory
import numpy as np
import json
from datetime import timedelta

def update_stock(stock, history_days=30):
    now = timezone.now()
    interval = timedelta(days=1)  # Assume we want to update every day

    # Ensure stock value isn't too small
    stock.value = max(stock.value, 0.1)

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
        daily_return = np.random.normal(0, 0.05)  # Reapply volatility
        new_price = round(stock.value * (1 + daily_return), 4)
        
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
    stocks = Stock.objects.all()
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
        # Check if the user has any stocks
        user_has_stock = Stock.objects.filter(owner=request.user).exists()
        context['user_has_stock'] = user_has_stock

    return render(request, 'stocks.html', context)


def stock_detail(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    update_stock(stock)

    stock_data_json = json.dumps({
        'color': stock.color,
        'data': list(stock.history.values('timestamp', 'price'))
    }, default=str)

    context = {
        'stock': stock,
        'stock_list': [stock],  # Pass as a list to use in the template
        'stock_data': stock_data_json,
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
            stock.owner = request.user  # Set the owner to the current user
            stock.save()
            return redirect('stock_home')  # Redirect to stock home or another appropriate page
    else:
        form = StockCreateForm()

    return render(request, 'create_stock.html', {'form': form})
