from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
#from accounts.forms import SignupForm
from django.contrib.auth.decorators import login_required, user_passes_test

######## For API Login 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            
            # Redirect to the home page after successful login
            next_url = request.GET.get('next', 'home')  # Redirect to the originally requested page
            return redirect(next_url)  # This should match the URL name for the home page
        else:
            # If authentication fails, show an error message and stay on the login page
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to the login page with error message
            
    return render(request, 'accounts/login.html')  # Render login page if GET request


# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from masters.models import UserProfile  # Ensure the path is correct
from masters.models import ShipmentDetail, StatusColor, ShipmentStatusHistory
from collections import defaultdict


def logout_view(request):
    logout(request)  # Logs out the user
    request.session.flush()  # Clears all session data
    return redirect('login')  # Redirect back to login page after logout

from django.shortcuts import redirect, render
from collections import defaultdict
from masters.models import UserProfile, ShipmentDetail, StatusColor

def home(request):
    user = request.user

    # Superusers and staff get the admin dashboard
    if user.is_staff or user.groups.filter(name="Imports Department").exists():
        return redirect('admin_dashboard')  # URL name for your admin dashboard

    # Get user's group
    groups = user.groups.all()
    user_profile = UserProfile.objects.filter(user=user).first()
    warehouse = user_profile.warehouse if user_profile and user_profile.warehouse else None

    # Shared logic for warehouse-related dashboards
    pending_status = StatusColor.objects.filter(status_name="Shipment created, not yet arrived").first()

    grouped_details = []
    if warehouse and pending_status:
        details = ShipmentDetail.objects.filter(
            status=pending_status,
            warehouse=warehouse
        ).select_related('shipment', 'item_category', 'shipment__company').order_by('shipment__expected_arrival_date')

        grouped = defaultdict(list)
        for d in details:
            grouped[(d.shipment.id, d.warehouse.warehouse_id)].append(d)

        for (shipment_id, warehouse_id), detail_list in grouped.items():
            first = detail_list[0]
            item_names = ", ".join(d.item_category.item_name for d in detail_list)
            grouped_details.append({
                'shipment': first.shipment,
                'warehouse': first.warehouse,
                'company': first.shipment.company,
                'expected_arrival_date': first.shipment.expected_arrival_date,
                'item_names': item_names,
                'detail_id': first.id,
            })

    context = {
        'user': user,
        'groups': groups,
        'warehouse': warehouse,
        'grouped_details': grouped_details,
        'show_common_masters_menu': user.groups.filter(name='Admin').exists()  # <-- add this
    }

    # Redirect to appropriate dashboards based on group
    if user.groups.filter(name="Warehouse Staff").exists():
       return redirect('warehouse_dashboard')
    elif user.groups.filter(name="Security Guard").exists():
        return render(request, 'dashboard/user_dashboard.html', context)
    elif user.groups.filter(name="Admin").exists():
        return redirect('admin_dashboard')  # URL name for your admin dashboard
    elif user.groups.filter(name="Managing Director").exists():
        return redirect('md_dashboard')  # URL name for your admin dashboard
    elif user.groups.filter(name="Bank Controller").exists():
        return redirect('shipment_list')  # URL name for your adm
    elif user.groups.filter(name="Bank Manager").exists():
        return redirect('shipment_list')  # URL name for your adm
    elif user.groups.filter(name="Clearing Agent").exists():
        return redirect('clearing_agent_shipments_view')
    else:
 
        # fallback - unauthorized or unknown role
        return render(request, 'dashboard/access_denied.html', context)
