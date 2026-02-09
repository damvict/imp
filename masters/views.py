from django.shortcuts import render

from django.utils import timezone
# Item Category
from django.shortcuts import render, redirect,get_object_or_404, redirect
from .models import ItemCategory
from .forms import ItemCategoryForm
from .forms import ItemWarehouseSelectionForm
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import VehicleType
from .forms import VehicleTypeForm  # Assuming you created this form

from .models import StatusColor
from .forms import StatusColorForm

from .models import SalesDivision
from .forms import SalesDivisionForm  # We'll create this form next

from .forms import ShipmentForm
from .models import Shipment

from .models import UserProfile

from django.contrib.auth.decorators import login_required
from .forms import BankControllerForm
from .forms import MarkPaymentForm


#from .forms import ShipmentArrivalForm
from .models import ShipmentStatusHistory

from django.db.models import F, ExpressionWrapper, DurationField, Avg

from datetime import timedelta
from .models import Shipment, ShipmentDetail
from django.core.mail import send_mail
from openpyxl import Workbook
from django.http import HttpResponse

from .forms import (
    ShipmentForm,
    BankDocForm,
    AssessmentForm,
    MarkPaymentForm,
    DutyApprovalForm,
   
)

from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Shipment, ShipmentPhase, ShipmentPhaseMaster, StatusColor
from datetime import datetime

from rest_framework import status
from .models import BankDocument, Settlement
from django.db import models

from .models import Currency
from .serializers import CurrencySerializer

from django.http import JsonResponse
import json

def itemcategory_list(request):
    categories = ItemCategory.objects.all()
    return render(request, 'masters/itemcategory_list.html', {'categories': categories})


def itemcategory_create(request):
    if request.method == "POST":
        form = ItemCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('itemcategory_list')
    else:
        form = ItemCategoryForm()
    return render(request, 'masters/itemcategory_form.html', {'form': form})

def itemcategory_edit(request, pk):
    category = get_object_or_404(ItemCategory, pk=pk)
    if request.method == 'POST':
        form = ItemCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('itemcategory_list')
    else:
        form = ItemCategoryForm(instance=category)
    return render(request, 'masters/itemcategory_form.html', {'form': form})

def itemcategory_delete(request, pk):
    category = get_object_or_404(ItemCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('itemcategory_list')
    return render(request, 'masters/itemcategory_confirm_delete.html', {'category': category})




########### Vehicle Types



# List all vehicle types
def vehicle_type_list(request):
    vehicle_types = VehicleType.objects.all()
    return render(request, 'masters/vehicle_type_list.html', {'vehicle_types': vehicle_types})

# Create a new vehicle type
def vehicle_type_create(request):
    if request.method == 'POST':
        form = VehicleTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_type_list')
    else:
        form = VehicleTypeForm()
    return render(request, 'masters/vehicle_type_form.html', {'form': form})

# Edit an existing vehicle type
def vehicle_type_edit(request, pk):
    vehicle_type = get_object_or_404(VehicleType, pk=pk)
    if request.method == 'POST':
        form = VehicleTypeForm(request.POST, instance=vehicle_type)
        if form.is_valid():
            form.save()
            return redirect('vehicle_type_list')
    else:
        form = VehicleTypeForm(instance=vehicle_type)
    return render(request, 'masters/vehicle_type_form.html', {'form': form})

# Delete a vehicle type
def vehicle_type_delete(request, pk):
    vehicle_type = get_object_or_404(VehicleType, pk=pk)
    if request.method == 'POST':
        vehicle_type.delete()
        return redirect('vehicle_type_list')
    return render(request, 'masters/vehicle_type_confirm_delete.html', {'vehicle_type': vehicle_type})



#################

############ status 



def status_color_list(request):
    status_colors = StatusColor.objects.all()
    return render(request, 'masters/status_color_list.html', {'status_colors': status_colors})


def status_color_create(request):
    if request.method == 'POST':
        form = StatusColorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('status_color_list')
    else:
        form = StatusColorForm()
    return render(request, 'masters/status_color_form.html', {'form': form})


def status_color_edit(request, pk):
    status_color = get_object_or_404(StatusColor, pk=pk)
    if request.method == 'POST':
        form = StatusColorForm(request.POST, instance=status_color)
        if form.is_valid():
            form.save()
            return redirect('status_color_list')
    else:
        form = StatusColorForm(instance=status_color)
    return render(request, 'masters/status_color_form.html', {'form': form})


def status_color_delete(request, pk):
    status_color = get_object_or_404(StatusColor, pk=pk)
    status_color.delete()
    return redirect('status_color_list')


############ Sales Division 

def salesdivision_list(request):
    divisions = SalesDivision.objects.all()
    return render(request, 'masters/salesdivision_list.html', {'divisions': divisions})

def salesdivision_create(request):
    if request.method == 'POST':
        form = SalesDivisionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salesdivision_list')
    else:
        form = SalesDivisionForm()
    return render(request, 'masters/salesdivision_form.html', {'form': form})

def salesdivision_edit(request, pk):
    division = get_object_or_404(SalesDivision, pk=pk)
    if request.method == 'POST':
        form = SalesDivisionForm(request.POST, instance=division)
        if form.is_valid():
            form.save()
            return redirect('salesdivision_list')
    else:
        form = SalesDivisionForm(instance=division)
    return render(request, 'masters/salesdivision_form.html', {'form': form})

def salesdivision_delete(request, pk):
    division = get_object_or_404(SalesDivision, pk=pk)
    division.delete()
    return redirect('salesdivision_list')
    
#####################################
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company
from .forms import CompanyForm  # Make sure this form exists

# List View
class CompanyListView(ListView):
    model = Company
    template_name = 'masters/company_list.html'
    context_object_name = 'companies'

# Create View
class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'masters/company_form.html'
    success_url = reverse_lazy('company_list')

# Update View
class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'masters/company_form.html'
    success_url = reverse_lazy('company_list')

# Delete View
class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'masters/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')

#################################################################

# views.py
def shipment_create(request):
    if request.method == 'POST':
        shipment_form = ShipmentForm(request.POST)
        item_warehouse_form = ItemWarehouseSelectionForm(request.POST)

        if shipment_form.is_valid() and item_warehouse_form.is_valid():
            shipment = shipment_form.save(commit=False)
            shipment.created_by = request.user
            shipment.save()

            

            #default_status = StatusColor.objects.get(status_id=1)
            default_status, created = StatusColor.objects.get_or_create(
                status_id=1,
                defaults={'status_name': 'Pending', 'color_code': '#FFA500'}
            )

            for combo in item_warehouse_form.cleaned_data['item_warehouses']:
                item_id, warehouse_id = map(int, combo.split('_'))
                item = ItemCategory.objects.get(pk=item_id)
                warehouse = Warehouse.objects.get(pk=warehouse_id)

                ShipmentDetail.objects.create(
                    shipment=shipment,
                    item_category=item,
                    warehouse=warehouse,
                    sales_division=item.sales_division,
                    status=default_status
                )

            return redirect('shipment_list')

    else:
        shipment_form = ShipmentForm()
        item_warehouse_form = ItemWarehouseSelectionForm()

    return render(request, 'masters/shipment_form.html', {
        'form': shipment_form,
        'item_warehouse_form': item_warehouse_form
    })



from django.shortcuts import render
from .models import ShipmentDetail
def shipment_list(request):
    shipments = ShipmentDetail.objects.select_related(
        'shipment', 'item_category', 'status', 'vehicle_type'
    ).exclude(
        status__status_name__iexact='Unloading completed'
    ).all().order_by('-shipment__created_at')

    # check if user is Bank Controller
    is_bank_controller = request.user.groups.filter(name="Bank Controller").exists()
    is_bank_Manager = request.user.groups.filter(name="Bank Manager").exists()

    return render(
        request,
        'masters/shipment_list.html',
        {
            'shipments': shipments,
            'is_bank_controller': is_bank_controller,  # pass flag to template
            'is_bank_Manager': is_bank_Manager,  # pass flag to template
        }
    )



@login_required
def pending_shipments(request):
    try:
        pending_status = StatusColor.objects.get(status_name="Shipment created, not yet arrived")
    except StatusColor.DoesNotExist:
        pending_status = None

    shipments = Shipment.objects.filter(status=pending_status).order_by('expected_arrival_date')
    return render(request, 'masters/pending_shipments_list.html', {'shipments': shipments})

@login_required
def shipment_edit(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)

    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)   # <-- instance=shipment
        if form.is_valid():
            form.save()
            return redirect('shipment_list')  # or wherever you want
    else:
        form = ShipmentForm(instance=shipment)   # <-- prefill with shipment

    return render(request, 'masters/shipment_form.html', {
        'form': form,
        'item_warehouse_form': None,  # if you need another form, pass it here
    })

@login_required
def shipment_delete(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    if request.method == 'POST':
        shipment.delete()
        return redirect('shipment_list')
    return render(request, 'masters/shipment_confirm_delete.html', {'shipment': shipment})


############################ shipments Pending vehicle update
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import ShipmentDetail, StatusColor, ShipmentStatusHistory

@login_required
@permission_required('masters.can_update_arrival_status', raise_exception=True)
def pending_arrival_list(request):
    pending_status = StatusColor.objects.filter(
        status_name="Shipment created, not yet arrived"
    ).first()

    details = (ShipmentDetail.objects
               .filter(status=pending_status)
               .select_related('shipment', 'item_category', 'shipment__company')
               .order_by('shipment__expected_arrival_date')
              ) if pending_status else ShipmentDetail.objects.none()


    return render(request,
                  'masters/pending_arrivals_list.html',
                  {'details': details})

@login_required
def pending_shipments(request):
    try:
        pending_status = StatusColor.objects.get(status_name="Shipment created, not yet arrived")
    except StatusColor.DoesNotExist:
        pending_status = None

    shipments = Shipment.objects.filter(status=pending_status).order_by('expected_arrival_date')
    return render(request, 'masters/pending_shipments_list.html', {'shipments': shipments})
    
############################################

def bank_controller_view(request):
    # Filter shipments same as your API
    shipments = Shipment.objects.filter(
        send_to_clearing_agent=False
    )

    return render(request, 'masters/bc_shipments.html', {'shipments': shipments})


@login_required
def bank_controller_update(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Ensure only Bank Controllers can access
    if not request.user.groups.filter(name="Bank Controller").exists():
        return redirect("shipment_list")  # Or raise PermissionDenied

    if request.method == "POST":
        form = BankControllerForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
################################

        # --- Send email notification ---
        subject = f"Shipment {shipment.id} Updated by Bank Controller"
        message = (
        f"Dear Team,\n\n"
        f"The shipment with ID {shipment.id} has been updated by {request.user.username}.\n\n"
        f"Regards,\n"
        f"Imports System"
        )
        from_email = "damvict@gmail.com"
        recipient_list = ["damayanthi.caipl@gmail.com"]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print("Email sending failed:", e)


######################### end of email

            #return redirect("shipment_list")  # After save, redirect
        return redirect('bank_controller_view')

    else:
        form = BankControllerForm(instance=shipment)

    return render(request, "masters/bank_controller_update.html", {"form": form, "shipment": shipment})


###############################################

############################################
@login_required
def bank_manager_update_original(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Ensure only Bank Controllers can access
    if not request.user.groups.filter(name="Bank Manager").exists():
        return redirect("shipment_list")  # Or raise PermissionDenied

    if request.method == "POST":
        form = MarkPaymentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            return redirect("shipment_list")  # After save, redirect
    else:
        form = BankControllerForm(instance=shipment)

    return render(request, "masters/bank_manager_update.html", {"form": form, "shipment": shipment})


def bank_manager_view(request):
    # Filter shipments same as your API
    shipments = Shipment.objects.filter(
        send_to_clearing_agent=True,
        payment_marked=False,
        c_ass_send=True

        
    )

    return render(request, 'dash/bank_manager_view.html', {'shipments': shipments})

def bank_manager_update(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == "POST":
        #print("DEBUG: POST data:", request.POST)

        shipment.send_date = request.POST.get("send_date") or None
        #print("DEBUG: send_date:", shipment.send_date)

        if "payment_marked" in request.POST:   # checkbox checked
            shipment.payment_marked = True
            if not shipment.payment_marked_date:   # only set once
                shipment.payment_marked_date = timezone.now().date()
            #print("DEBUG: payment_marked checked, date:", shipment.payment_marked_date)
        else:
            shipment.payment_marked = False
            shipment.payment_marked_date = None
            #print("DEBUG: payment_marked unchecked")

        shipment.save()
        #print("DEBUG: Shipment saved:", shipment.id)

        return redirect("bank_manager_view")




############################ Clearing Agent Update  ###################
# views.py
from django.shortcuts import render, get_object_or_404, redirect

from .models import Shipment
from .forms import AssessmentUploadForm  # We'll create this form

def clearing_agent_shipments_view(request):
   
    shipments = Shipment.objects.filter(
        send_to_clearing_agent=True,
        payment_marked=False
    )

    #return render(request, 'masters/clearing_agent_shipments.html', {'shipments': shipments})
    if request.method == "POST":
        # Loop through shipments to save total duty values
        for shipment in shipments:
            duty_value = request.POST.get(f"total_duty_{shipment.id}")
            if duty_value:
                shipment.total_duty_value = duty_value
                shipment.save()
        return redirect("clearing_agent_shipments_view")

    return render(request, "masters/clearing_agent_shipments.html", {
        "shipments": shipments
    })



# views.py
def upload_assessment_document_view(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == 'POST':
        form = AssessmentUploadForm(request.POST, request.FILES, instance=shipment)
        duty_value = request.POST.get(f"total_duty_{shipment.id}")
        if form.is_valid():
            shipment.assessment_uploaded_date = timezone.now().date()
            shipment.total_duty_value = duty_value
            form.save()
            return redirect('clearing_agent_shipments_view')  # Redirect back to list
    else:
        form = AssessmentUploadForm(instance=shipment)

    return render(request, 'masters/upload_assessment_document.html', {
        'form': form,
        'shipment': shipment
    })

#####################


@login_required
def shipment_arrival_update(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)

    if request.method == 'POST':
        form = ShipmentArrivalForm(request.POST, instance=shipment)
        if form.is_valid():
            shipment = form.save(commit=False)

            # Update status to "Arrived"
            try:
                arrived_status = StatusColor.objects.get(status_name="Shipment arrived at warehouse")
                shipment.status = arrived_status
            except StatusColor.DoesNotExist:
                pass  # Optionally handle if status missing

            shipment.save()

            # Record status history
            ShipmentStatusHistory.objects.create(
                shipment=shipment,
                status=shipment.status,
                updated_by=request.user,
                remarks=shipment.remarks
            )

            return redirect('pending_shipments')
    else:
        form = ShipmentArrivalForm(instance=shipment)

    return render(request, 'masters/shipment_arrival_form.html', {'form': form, 'shipment': shipment})


############################ Pending Unloading
@login_required
def pending_unloading_list(request):
    unloading_status = StatusColor.objects.get(status_name="Shipment arrived at warehouse")
    pending_shipments = ShipmentDetail.objects.filter(
        status=unloading_status,
        unloading_start_time__isnull=True
    ).distinct()

    return render(request, 'masters/pending_unloading_list.html', {
        'pending_shipments': pending_shipments
    })


@login_required


def start_unloading(request, pk):
    # Get the current shipment detail
    shipment_detail = get_object_or_404(ShipmentDetail, pk=pk)

    # Get the desired status object
    unloading_status = StatusColor.objects.get(status_name="Currently being unloaded")

    # Get all records with same shipment_id and warehouse_id
    matching_details = ShipmentDetail.objects.filter(
        shipment=shipment_detail.shipment,
        warehouse=shipment_detail.warehouse
    )

    # Update each record
    for detail in matching_details:
        detail.unloading_start_time = timezone.now()
        detail.status = unloading_status
        detail.save()

        # Record status history
        ShipmentStatusHistory.objects.create(
            shipment=detail.shipment,
            status=unloading_status,
            updated_by=request.user
        )

    messages.success(request, "Unloading started successfully for all matching records.")

    #return redirect('masters:pending_unloading_list')  # ✅ Use correct URL name
    return redirect('pending_unloading_list')
    
############ Finish Loading 
@login_required
def unloading_in_progress_list(request):
    status = StatusColor.objects.get(status_name="Currently being unloaded")
    shipments = ShipmentDetail.objects.filter(status=status)
    return render(request, 'masters/unloading_in_progress_list.html', {'shipments': shipments})
    

def finish_unloading(request, pk):
    # Get the reference ShipmentDetail using pk
    shipment_detail = get_object_or_404(ShipmentDetail, pk=pk)

    # Get the related shipment_id and warehouse_id
    shipment_id = shipment_detail.shipment_id
    warehouse_id = shipment_detail.warehouse_id

    # Get the status object for "Unloading completed"
    unloaded_status = StatusColor.objects.get(status_name="Unloading completed")

    # Update all ShipmentDetail records with same shipment_id and warehouse_id
    ShipmentDetail.objects.filter(
        shipment_id=shipment_id,
        warehouse_id=warehouse_id
    ).update(
        unloading_end_time=timezone.now(),
        status=unloaded_status
    )

    # Save status history for tracking
    ShipmentStatusHistory.objects.create(
        shipment=shipment_detail.shipment,
        status=unloaded_status,
        updated_by=request.user
    )

    # Redirect to the appropriate page (fix name if different)
    return redirect('warehouse_dashboard')

#########################3
###################### warehouse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Warehouse
from .forms import WarehouseForm

# List View
class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'masters/warehouse_list.html'
    context_object_name = 'warehouses'

# Create View
class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'masters/warehouse_form.html'
    success_url = reverse_lazy('warehouse_list')

# Update View
class WarehouseUpdateView(UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'masters/warehouse_form.html'
    success_url = reverse_lazy('warehouse_list')

# Delete View
class WarehouseDeleteView(DeleteView):
    model = Warehouse
    template_name = 'masters/warehouse_confirm_delete.html'
    success_url = reverse_lazy('warehouse_list')

#####################################     Supplier   ########################################################
from .models import Supplier
from .forms import SupplierForm  # you’ll create this next

# --- List View ---
class SupplierListView(ListView):
    model = Supplier
    template_name = 'masters/supplier_list.html'
    context_object_name = 'suppliers'


# --- Create View ---
class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'masters/supplier_form.html'
    success_url = reverse_lazy('supplier_list')


# --- Update View ---
class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'masters/supplier_form.html'
    success_url = reverse_lazy('supplier_list')


# --- Delete View ---
class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'masters/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')


############################  Clearing Agents #########
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ClearingAgent
from .forms import ClearingAgentForm


# List View
class ClearingAgentListView(ListView):
    model = ClearingAgent
    template_name = 'masters/clearingagent_list.html'
    context_object_name = 'agents'


# Create View
class ClearingAgentCreateView(CreateView):
    model = ClearingAgent
    form_class = ClearingAgentForm
    template_name = 'masters/clearingagent_form.html'
    success_url = reverse_lazy('clearingagent_list')


# Update View
class ClearingAgentUpdateView(UpdateView):
    model = ClearingAgent
    form_class = ClearingAgentForm
    template_name = 'masters/clearingagent_form.html'
    success_url = reverse_lazy('clearingagent_list')


# Delete View
class ClearingAgentDeleteView(DeleteView):
    model = ClearingAgent
    template_name = 'masters/clearingagent_confirm_delete.html'
    success_url = reverse_lazy('clearingagent_list')


##################### Reports

@login_required
def average_unloading_time_report(request):
    shipments_with_times = Shipment.objects.filter(
        unloading_start_time__isnull=False,
        unloading_end_time__isnull=False
    ).annotate(
        unloading_duration=ExpressionWrapper(
            F('unloading_end_time') - F('unloading_start_time'),
            output_field=DurationField()
        )
    )

    average_time = shipments_with_times.aggregate(avg_time=Avg('unloading_duration'))['avg_time']

    context = {
        'average_time': average_time,
        'shipments': shipments_with_times
    }
    return render(request, 'reports/average_unloading_time.html', context)
    
    ############### users

from django.contrib.auth.models import User
from .forms import UserCreateForm
from django.contrib import messages


def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # assign groups
            groups = form.cleaned_data['groups']
            user.groups.set(groups)
            
            # assign warehouses
            # Create UserProfile and assign selected warehouse
            selected_warehouse = form.cleaned_data['warehouse']
            UserProfile.objects.create(user=user, warehouse=selected_warehouse)

            messages.success(request, 'User created successfully.')
            return redirect('user_list')  # or wherever you want
        else:
             messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreateForm()

    return render(request, 'masters/create_user.html', {'form': form})

 
#@group_required('Imports Department')
def user_list(request):
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    #users = User.objects.all().order_by('-date_joined')
    return render(request, 'masters/user_list.html', {'users': users})
    

#!!!!!!!!!!!!!!!edit user

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = getattr(user, 'userprofile', None)

    if request.method == 'POST':
        form = UserCreateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            
            user.groups.set(form.cleaned_data['groups'])

            # Update or create user profile
            selected_warehouse = form.cleaned_data['warehouse']
            if user_profile:
                user_profile.warehouse = selected_warehouse
                user_profile.save()
            else:
                UserProfile.objects.create(user=user, warehouse=selected_warehouse)

            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
    else:
        initial_data = {
            'warehouse': user_profile.warehouse if user_profile else None,
            'groups': user.groups.all()
        }
        form = UserCreateForm(instance=user, initial=initial_data)

    return render(request, 'masters/edit_user.html', {'form': form, 'user_id': user.id})

#!!!!!!!!!!!!!!!!delete use
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')
    return render(request, 'masters/confirm_delete_user.html', {'user': user})

#!!!!!!!!!!! change password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def change_user_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps the user logged in
            messages.success(request, 'Password updated successfully.')
            return redirect('user_list')
    else:
        form = PasswordChangeForm(user)

    return render(request, 'masters/change_password.html', {'form': form, 'user': user})





####################### Pending
# Pending shipment list (awaiting arrivals)
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import ShipmentDetail, StatusColor, ShipmentStatusHistory
import logging
logger = logging.getLogger(__name__)

@login_required
@permission_required('masters.can_update_arrival_status', raise_exception=True)
def pending_arrival_list(request):
    pending_status = StatusColor.objects.filter(
        status_name="Shipment created, not yet arrived"
    ).first()

    details = (ShipmentDetail.objects
               .filter(status=pending_status)
               .select_related('shipment', 'item_category', 'shipment__company')
               .order_by('shipment__expected_arrival_date')
              ) if pending_status else ShipmentDetail.objects.none()


    return render(request,
                  'masters/pending_arrivals_list.html',
                  {'details': details})   
                  
                  
                  
######################

from .forms import ArrivalUpdateForm

@login_required
@permission_required('masters.can_update_arrival_status', raise_exception=True)
def arrival_update_detail(request, detail_id):
    detail = get_object_or_404(ShipmentDetail, pk=detail_id)

    if request.method == 'POST':
        form = ArrivalUpdateForm(request.POST, instance=detail)
        if form.is_valid():
            updated_detail = form.save(commit=False)
            try:
                arrived_status = StatusColor.objects.get(pk=2)
                updated_detail.status = arrived_status
            except StatusColor.DoesNotExist:
                messages.error(request, "Arrival status not found.")
                return redirect('masters:arrival_update_form.html')  # fix your redirect here!

            updated_detail.save()

            # Bulk update all ShipmentDetails with same shipment, warehouse, vehicle_type and vehicle_number
            ShipmentDetail.objects.filter(
                shipment=updated_detail.shipment,
                warehouse=updated_detail.warehouse,
             
            ).update(
                status=arrived_status,
                actual_arrival_date=updated_detail.actual_arrival_date,
                unloading_start_time=updated_detail.unloading_start_time,
                unloading_end_time=updated_detail.unloading_end_time,
                remarks=updated_detail.remarks,
                is_delayed=updated_detail.is_delayed,
                delay_reason=updated_detail.delay_reason,
                demurrage_start_date=updated_detail.demurrage_start_date,
                demurrage_end_date=updated_detail.demurrage_end_date,
                demurrage_amount=updated_detail.demurrage_amount,
                vehicle_type=updated_detail.vehicle_type,
                vehicle_number=updated_detail.vehicle_number,
            )

            # Create history records for each updated ShipmentDetail (optional)
            for shipment_detail in ShipmentDetail.objects.filter(
                shipment=updated_detail.shipment,
                warehouse=updated_detail.warehouse,
                vehicle_type=updated_detail.vehicle_type,
                vehicle_number=updated_detail.vehicle_number,
            ):
                ShipmentStatusHistory.objects.create(
                    shipment=shipment_detail.shipment,
                    status=arrived_status,
                    updated_by=request.user
                )

            return redirect('pending_arrival_list')

    else:
        form = ArrivalUpdateForm(instance=detail)

    return render(request, 'masters/arrival_update_form.html', {
        'form': form,
        'detail': detail
    })

    
    
    
#################### Dashboard - warehouse 
from django.db.models import Count
from django.contrib.auth.decorators import login_required


from masters.models import StatusColor, ShipmentDetail, UserProfile



    ####################### dashboard warehousefrom django.http import JsonResponse

@login_required
def warehouse_dashboard_api(request):
    today = timezone.now().date()

    inbound_shipments = Shipment.objects.filter(
        C_Process_completed=True,
        arrival_at_warehouse=False
    ).count()

    pending_grn = Shipment.objects.filter(
        arrival_at_warehouse=True,
        grn_complete_at_warehouse=False
    ).count()

    record_grn = Shipment.objects.filter(
        arrival_at_warehouse=True,
        grn_upload_at_warehouse=False
    ).count()

    confirm_grn = Shipment.objects.filter(
        grn_upload_at_warehouse=True,
        grn_complete_at_warehouse=False
    ).count()

    grn_completed = Shipment.objects.filter(
        grn_complete_at_warehouse=True,
        grn_complete_at_warehouse_date__month=today.month,
        grn_complete_at_warehouse_date__year=today.year
    ).count()

    overdue_shipments = Shipment.objects.filter(
        expected_arrival_date__lt=today,
        arrival_at_warehouse=False
    ).count()

    return JsonResponse({
        "inbound_shipments": inbound_shipments,
        "pending_grn": pending_grn,
        "record_grn": record_grn,
        "confirm_grn": confirm_grn,
        "grn_completed": grn_completed,
        "overdue_shipments": overdue_shipments,
    })

def build_warehouse_timeline(shipment):
    return [
        {
            "label": "Arrival at Warehouse",
            "done": shipment.arrival_at_warehouse,
            "date": shipment.arrival_at_warehouse_date,
            "icon": "truck",
        },
        {
            "label": "Truck Departure",
            "done": shipment.departure_at_warehouse,
            "date": shipment.departure_at_warehouse_date,
            "icon": "arrow-right",
        },
        {
            "label": "GRN Uploaded",
            "done": shipment.grn_upload_at_warehouse,
            "date": shipment.grn_upload_at_warehouse_date,
            "icon": "file-text",
        },
        {
            "label": "GRN Completed",
            "done": shipment.grn_complete_at_warehouse,
            "date": shipment.grn_complete_at_warehouse_date,
            "icon": "check-circle",
        },
    ]


@login_required
def warehouse_dashboard(request):
    today = timezone.localdate()
    

    current_month_filter = Q(
        order_date__year=today.year,
        order_date__month=today.month
    )

    context = {
        "today": today,

        # Inbound shipments
        "inbound_shipments": Shipment.objects.filter(
            C_Process_completed=True,
            arrival_at_warehouse=False
        ).count(),

        # Monthly stats
        "total_shipments_month": Shipment.objects.filter(
            current_month_filter,
            ship_status__gt=1
        ).count(),

        "completed_shipments": Shipment.objects.filter(
            ship_status=13
        ).count(),

        "active_shipments": Shipment.objects.filter(
            ship_status__lt=13
        ).count(),

        # GRN stats
        "pending_grn": Shipment.objects.filter(
            arrival_at_warehouse=True,
            grn_complete_at_warehouse=False
        ).count(),

        "record_grn": Shipment.objects.filter(
            arrival_at_warehouse=True,
            grn_upload_at_warehouse=False
        ).count(),

        "confirm_grn": Shipment.objects.filter(
            grn_upload_at_warehouse=True,
            grn_complete_at_warehouse=False
        ).count(),

        "grn_completed": Shipment.objects.filter(
            grn_complete_at_warehouse=True,
            grn_complete_at_warehouse_date__year=today.year,
            grn_complete_at_warehouse_date__month=today.month
        ).count(),

        # Arriving today (DISPATCHED TODAY)
        "arriving_today": Shipment.objects.filter(
            ship_dispatch=True,
            ship_dispatch_date__date=today
        ).count(),
    }

    shipments = Shipment.objects.filter(
    ship_dispatch=True
    ).exclude(
        ship_status=13
    )


    shipment_timelines = []
    for s in shipments:
        shipment_timelines.append({
                "shipment": s,
                "timeline": build_warehouse_timeline(s)
    })

    context["shipment_timelines"] = shipment_timelines

    
    return render(request, "dash/ws_dashboard.html", context)



@login_required
def warehouse_dashboard_old(request):
    today = timezone.now().date()

    # Get the user's assigned warehouse
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_warehouse = user_profile.warehouse
    except UserProfile.DoesNotExist:
        user_warehouse = None

    if not user_warehouse:
        return render(request, 'dash/ws_dashboard.html', {
            'error': 'No warehouse assigned to your profile.'
        })

    # Get predefined statuses
    pending_status = StatusColor.objects.filter(status_name__iexact="Shipment created, not yet arrived").first()
    arrived_status = StatusColor.objects.filter(status_name="Shipment arrived at warehouse").first()
    unloading_status = StatusColor.objects.filter(status_name__iexact="Currently being unloaded").first()
    delivered_status = StatusColor.objects.filter(status_name__iexact="Unloading completed").first()

    # Shipments Awaiting Arrival
    shipments_awaiting = ShipmentDetail.objects.filter(
        status=pending_status,
        warehouse=user_warehouse
    ).values('shipment').distinct().count() if pending_status else 0

    # Arrived Shipments (Count and List)
    arrived_shipments = ShipmentDetail.objects.filter(
        status=arrived_status,
        warehouse=user_warehouse
    ).values('shipment').distinct().count() if arrived_status else 0

    arrived_shipments_list = ShipmentDetail.objects.filter(
        status=arrived_status,
        warehouse=user_warehouse
    ).select_related('shipment', 'item_category', 'vehicle_type').distinct() if arrived_status else []

    # Currently Unloading
    currently_unloading = ShipmentDetail.objects.filter(
        status=unloading_status,
        warehouse=user_warehouse
    ).values('shipment').distinct().count() if unloading_status else 0
    
    
    # Full list of currently unloading shipments
    currently_unloading_shipments = ShipmentDetail.objects.filter(
        status=unloading_status,
        warehouse=user_warehouse
    ).select_related('shipment', 'status').distinct() if unloading_status else []

    # Completed Shipments Today
    shipments_delivered_today = ShipmentDetail.objects.filter(
        status=delivered_status,
        actual_arrival_date=today,
        warehouse=user_warehouse
    ).values('shipment').distinct().count() if delivered_status else 0

    # Pie chart data
    shipments_by_status = ShipmentDetail.objects.filter(
        warehouse=user_warehouse
    ).values('status__status_name').annotate(count=Count('id'))

    # Total shipments that are either arrived or being unloaded
    total_shipments_current = ShipmentDetail.objects.filter(
        status__status_name__in=['Shipment arrived at warehouse', 'Currently being unloaded'],
        warehouse=user_warehouse
    ).values('shipment').distinct().count()

    # Delayed shipments
    delayed_shipments = ShipmentDetail.objects.filter(
        is_delayed=True,
        warehouse=user_warehouse
    ).values('shipment').distinct().count()

    # Pending list
    pending_arrival_list = ShipmentDetail.objects.filter(
        status=pending_status,
        warehouse=user_warehouse
    ).select_related('shipment', 'vehicle_type', 'status').distinct() if pending_status else []

    # Final context
    context = {
        'shipments_awaiting': shipments_awaiting,
        'arrived_shipments': arrived_shipments,
        'arrived_shipments_list': arrived_shipments_list,
        'currently_unloading': currently_unloading,
        'currently_unloading_shipments':currently_unloading_shipments,
        'shipments_delivered_today': shipments_delivered_today,
        'shipments_by_status': shipments_by_status,
        'total_shipments_current': total_shipments_current,
        'delayed_shipments': delayed_shipments,
        'warehouse': user_warehouse,
        'pending_arrival_list': pending_arrival_list,
    }

    return render(request, 'dash/warehouse_dashboard.html', context)
######################## Admin Dashboard

from .models import ShipmentDetail
from django.db.models import OuterRef, Subquery
from collections import defaultdict
from datetime import datetime
from django.db.models import Count

from django.utils.timezone import make_aware, get_current_timezone
default_time = make_aware(datetime.min, get_current_timezone())

def admin_dashboard(request):
    # Fetch all shipment details
    details = ShipmentDetail.objects.select_related(
        'shipment', 'status', 'warehouse', 'vehicle_type', 'item_category'
    ).order_by('-unloading_start_time')

    # Group by unique (shipment_id, warehouse_id)
    grouped = defaultdict(list)
    for d in details:
        grouped[(d.shipment.id, d.warehouse.warehouse_id)].append(d)

    # Prepare recent 10 grouped records
    grouped_details = []
    for (shipment_id, warehouse_id), detail_list in grouped.items():
        first = detail_list[0]
        item_names = ", ".join(d.item_category.item_name for d in detail_list if d.item_category)
        grouped_details.append({
            'shipment': first.shipment,
            'shipment_id': first.shipment.id,
            'warehouse': first.warehouse,
            'status': first.status,
            'vehicle_number': first.vehicle_number,
            'unloading_start_time': first.unloading_start_time,
            'unloading_end_time': first.unloading_end_time,
            'item_names': item_names,
        })

    # Sort and limit to 10 recent
    grouped_details = sorted(
    grouped_details,
    key=lambda x: x['unloading_start_time'] or default_time,
    reverse=True
    )[:10]
    #grouped_details = sorted(grouped_details, key=lambda x: x['unloading_start_time'] or '', reverse=True)[:10]
    #grouped_details = sorted(grouped_details, key=lambda x: x['unloading_start_time'] or datetime.min, reverse=True)[:10]
    # Count logic
    def count_by_status(name):
        return ShipmentDetail.objects.filter(status__status_name=name).values('shipment_id', 'warehouse_id').distinct().count()

    total_shipments = ShipmentDetail.objects.values('shipment_id', 'warehouse_id').distinct().count()
    pending_arrivals = count_by_status("Shipment created, not yet arrived")
    pending_unloading = count_by_status("Pending unloading")
    unloading_shipments = count_by_status("Currently being unloaded")
    unloaded_shipments = count_by_status("Unloading completed")
    delayed_shipments = ShipmentDetail.objects.filter(is_delayed=True).values('shipment_id', 'warehouse_id').distinct().count()

    context = {
        'total_shipments': total_shipments,
        'pending_arrivals': pending_arrivals,
        'pending_unloading': pending_unloading,
        'unloading_shipments': unloading_shipments,
        'delayed_shipments': delayed_shipments,
        'unloaded_shipments': unloaded_shipments,
        'recent_shipments': grouped_details
    }

    return render(request, 'dash/admin_dashboard.html', context)



# masters/views.py


def shipment_stage_times_report(request):
    shipments = Shipment.objects.all()  # Or your query
    return render(request, "reports/shipment_stage_times_report.html", {"shipments": shipments})


def shipment_stage_times_report_pdf(request):
    shipments = Shipment.objects.all().order_by('created_at')
    
    html_string = render_to_string('reports/shipment_stage_times_report.html', {
        'shipments': shipments
    })
    
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="shipment_stage_times_report.pdf"'
    return response

################ md_Dashboard

def is_md(user):
    return user.groups.filter(name="Managing Director").exists()


from django.utils.timezone import now

@login_required
@user_passes_test(is_md)
def md_dashboard(request):   
    today = now()
    payment_app = Shipment.objects.filter(
        payment_marked=True,
        duty_paid=False
    ).count()
    total_invoice_value = (
        Shipment.objects.aggregate(total=Sum("amount"))["total"] or 0
    )

    clearance_initiated = Shipment.objects.filter(
        C_Process_Initiated=True,
        C_Process_completed=False
    ).count()

    clearance_completed = Shipment.objects.filter(
        C_Process_completed=True
    ).count()

    approved_duty_payments = Shipment.objects.filter(
        duty_paid=True
    ).count()

    pending_grn = Shipment.objects.filter(
        arrival_at_warehouse=True,
        grn_complete_at_warehouse=False
    ).count()

    total_grn_value_month = (
        Shipment.objects.filter(
            grn_complete_at_warehouse_date__month=today.month,
            grn_complete_at_warehouse_date__year=today.year
        ).aggregate(total=Sum("amount"))["total"] or 0
    )

    payment_app = Shipment.objects.filter(
        payment_marked=True,
        duty_paid=False
    ).count()

    overview = {
        "total_invoice_value": total_invoice_value,
        "clearance_initiated": clearance_initiated,
        "clearance_completed": clearance_completed,
        "approved_duty_payments": approved_duty_payments,
        "pending_grn": pending_grn,
        "total_grn_value_month": total_grn_value_month,
    }



    context = {
        "overview": overview,
        "md": {
            "payment_app": payment_app
        }
    }

    return render(
        request,
        "dash/md_dashboard.html",
        context
    )

############################################

from .models import Bank, BankDocument
from django.db.models import Sum, Q


def md_bank_dashboard(request):
    banks = Bank.objects.all()
    data = []

    for bank in banks:
        # Total used amounts from BankDocument (only unsettled)
        lc_used = BankDocument.objects.filter(
            bank=bank,
            doc_type='LC',
            settled=False
        ).aggregate(total=Sum('amount'))['total'] or 0

        imp_used = BankDocument.objects.filter(
            bank=bank,
            doc_type='IMP',
            settled=False
        ).aggregate(total=Sum('amount'))['total'] or 0

        da_used = BankDocument.objects.filter(
            bank=bank,
            doc_type='DA',
            settled=False
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Calculate balances (limit - used)
        lc_balance = (bank.lc or 0) - lc_used
        imp_balance = (bank.imp or 0) - imp_used
        da_balance = (bank.da or 0) - da_used

        # Percent used
        lc_percent = ((lc_used / bank.lc) * 100) if bank.lc else 0
        imp_percent = ((imp_used / bank.imp) * 100) if bank.imp else 0
        da_percent = ((da_used / bank.da) * 100) if bank.da else 0

        data.append({
            'bank_name': bank.b_name,
            'od': bank.od or 0,
            'lc_limit': bank.lc or 0,
            'lc_balance': lc_balance,
            'lc_percent': round(lc_percent, 2),
            'imp_limit': bank.imp or 0,
            'imp_balance': imp_balance,
            'imp_percent': round(imp_percent, 2),
            'da_limit': bank.da or 0,
            'da_balance': da_balance,
            'da_percent': round(da_percent, 2),
        })

    context = {'bank_data': data}
    return render(request, "dash/md_bank_dashboard.html", context)




###############################

def approve_duty_paid_md(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if not shipment.payment_marked:
        messages.error(request, "Payment not marked yet. Cannot approve duty.")
        return redirect("md_dashboard")

    shipment.duty_paid = True
    shipment.duty_paid_date = timezone.now().date()
    shipment.save()

    messages.success(request, f"Duty approved successfully for Shipment {shipment.id}")
    return redirect("md_dashboard")


##################### Reject Duty Paid MD
from django.contrib import messages
@login_required
def reject_duty_paid_web(request, shipment_id):
    if request.method != "POST":
        messages.error(request, "Invalid request method")
        return redirect("md_dashboard")

    shipment = get_object_or_404(Shipment, id=shipment_id)

    # --- SAME CHECK AS API ---
    if not shipment.payment_marked:
        messages.error(request, "Payment not marked yet")
        return redirect(request.META.get("HTTP_REFERER", "md_dashboard"))

    reason = request.POST.get("reason", "").strip()
    if not reason:
        messages.error(request, "Rejection reason is required")
        return redirect(request.META.get("HTTP_REFERER", "md_dashboard"))

    # --- SAME REJECT LOGIC AS API ---
    shipment.duty_paid = False
    shipment.duty_paid_reject = True
    shipment.md_reject_reason = reason
    shipment.md_rejected_at = timezone.now()
    print("BEFORE REJECT:", shipment.payment_marked)
    shipment.payment_marked = False
    shipment.payment_marked_date = None

    shipment.save()

    messages.success(request, "Duty rejected successfully")
    print("AFTER REJECT:", shipment.payment_marked)
    return redirect(request.META.get("HTTP_REFERER", "md_dashboard"))





################################ API ##############
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#from .models import Shipment
from .serializers import ClearingAgentShipmentSerializer,arrival_notice_listSerializer
from .serializers import MDShipmentSerializer
from .serializers import BankManagerShipmentSerializer
from .serializers import WarehouseSerializer
from .serializers import BankManagerpaySerializer
from .serializers import BankManagerpayrefSerializer

from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clearing_agent_shipments(request):
    shipments = Shipment.objects.filter(
         clearing_agent=request.user,
        send_to_clearing_agent=True
    ).filter(
        Q(assessment_document__isnull=True) | Q(assessment_document='')
    )
    serializer = ClearingAgentShipmentSerializer(shipments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clearing_agent_shipments_pay_uploaded(request):
    # Filter shipments: payment sent to clearing agent, clearing not initiated
    shipments = Shipment.objects.filter(
        send_to_clearing_agent_payment=True,
        clearing_agent=request.user,
        C_Process_Initiated=0   
    )

    serializer = ClearingAgentShipmentSerializer(shipments, many=True)
    return Response(serializer.data)

############## Currency
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def currencies_list(request):
    currencies = Currency.objects.filter(is_active=True).order_by("code")
    serializer = CurrencySerializer(currencies, many=True)
    return Response(serializer.data)

##~~~~~~~~~~~


### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Clearing Agent Inttiate Clearence ~~~~~~~~~~~~~~~~~~~~~~

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def C_Process_Initiated(request, shipment_id):
  
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

       
    shipment.C_Process_Initiated = True
    shipment.C_Process_Initiated_date = timezone.now()
    shipment.save()

    # ---- Create ShipmentPhase record for handover ----
    try:
        phase_master = ShipmentPhaseMaster.objects.get(id=8)  # adjust ID
        ShipmentPhase.objects.create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )
    except ShipmentPhaseMaster.DoesNotExist:
        # Optional: skip or log error if phase master not found
        pass

    serializer = ClearingAgentSerializer(shipment)
    return Response(
        {"success": True, 
         "message": "Clearing Process Initiated successfully", "shipment": serializer.data},
        status=status.HTTP_200_OK
    )










    ################################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def arrival_notice_list(request):
    shipments = Shipment.objects.filter(
       ship_status=1
    ).filter(
        Q(assessment_document__isnull=True) | Q(assessment_document='')
    )
    serializer = arrival_notice_listSerializer(shipments, many=True)
    return Response(serializer.data)

#### Upload assensment
# views.py
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Shipment

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_assessment_document(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    total_duty = request.data.get("total_duty_value")
    file = request.FILES.get("assessment_document")
    

    # ❌ File is mandatory
    if not file:
        return Response(
            {"error": "Assessment document is mandatory"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ Create phase (only when file is uploaded)
    try:
        phase_master = ShipmentPhaseMaster.objects.get(id=4)
        ShipmentPhase.objects.get_or_create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            defaults={
                "phase_name": phase_master.phase_name,
                "completed": True,
                "completed_at": timezone.now(),
                "updated_by": request.user,
                "order": phase_master.order,
            }
        )
    except ShipmentPhaseMaster.DoesNotExist:
        return Response({"error": "Phase master not found"}, status=400)

    # ✅ Save assessment
    shipment.assessment_document = file
    shipment.total_duty_value = total_duty
    shipment.assessment_uploaded_date = timezone.now()
    shipment.c_ass_send = True
    shipment.save()

    return Response(
        {"message": "Assessment uploaded successfully"},
        status=status.HTTP_200_OK
    )





#########
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank_manager_shipments(request):
    """
    List shipments that have assessment document uploaded but payment not marked yet
    """
    shipments = Shipment.objects.filter(
        assessment_document__isnull=False,
        payment_marked=False
    )
    serializer = BankManagerShipmentSerializer(shipments, many=True)
    return Response(serializer.data)

#----------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank_manager_payment_reference(request):
    """
    List shipments that have assessment document uploaded but payment not marked yet
    """
    shipments = Shipment.objects.filter(
        duty_paid=True,
        send_to_clearing_agent_payment=False
    )
    serializer = BankManagerpaySerializer(shipments, many=True)
    return Response(serializer.data)





from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_payment_done(request, shipment_id):
    """
    Marks the shipment as paid, updates bank/payment info,
    and logs the shipment phase (handover to next stage).
    Expects JSON payload:
    {
        "duty_paid_bank": "Bank ABC",
        "payment_type": "BT",  # BT / LC / CP
        "pay_note": "Some notes"
    }
    """
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    duty_paid_bank = data.get("duty_paid_bank")
    payment_type = data.get("payment_type")
    pay_note = data.get("pay_note")

    # Update payment info if provided
    if duty_paid_bank is not None:
        shipment.duty_paid_bank = duty_paid_bank
    if payment_type in dict(Shipment.PAYMENT_TYPES):
        shipment.payment_type = payment_type
    if pay_note is not None:
        shipment.pay_note = pay_note

    # Mark payment done
    shipment.payment_marked = True
    shipment.payment_marked_date = timezone.now()
    shipment.save()

    # ---- Create ShipmentPhase record for handover ----
    try:
        phase_master = ShipmentPhaseMaster.objects.get(id=5)  # adjust ID
        ShipmentPhase.objects.create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )
    except ShipmentPhaseMaster.DoesNotExist:
        # Optional: skip or log error if phase master not found
        pass

    serializer = BankManagerShipmentSerializer(shipment)
    return Response(
        {"message": "Payment marked successfully", "shipment": serializer.data},
        status=status.HTTP_200_OK
    )


import uuid
import os
import os

from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from masters.models import Shipment, ShipmentPhase, ShipmentPhaseMaster
from masters.serializers import BankManagerpayrefSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bm_update_payment_ref(request, shipment_id):
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

    payref_document_ref = request.data.get("payref_document_ref")
    file = request.FILES.get("payref_document")

    if not payref_document_ref:
        return Response({"error": "Payment reference is required"}, status=status.HTTP_400_BAD_REQUEST)

    if file:
        if file.size > 10 * 1024 * 1024:
            return Response({"error": "File too large (limit 10MB)"}, status=status.HTTP_400_BAD_REQUEST)

        # Delete old document if exists
        if shipment.payref_document and hasattr(shipment.payref_document, "path") and os.path.isfile(shipment.payref_document.path):
            os.remove(shipment.payref_document.path)

        shipment.payref_document = file

    shipment.payref_document_ref = payref_document_ref
    shipment.send_to_clearing_agent_payment = True
    shipment.send_to_clearing_agent_payment_date = timezone.now()

    # Save safely in transaction
    try:
        with transaction.atomic():
            shipment.save()

            # Optional phase tracking
            try:
                phase_master = ShipmentPhaseMaster.objects.get(id=7)
                ShipmentPhase.objects.create(
                    shipment=shipment,
                    phase_code=phase_master.phase_code,
                    phase_name=phase_master.phase_name,
                    completed=True,
                    completed_at=timezone.now(),
                    updated_by=request.user,
                    order=phase_master.order,
                )
            except ShipmentPhaseMaster.DoesNotExist:
                pass

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ Always return response after try block
    serializer = BankManagerpayrefSerializer(shipment, context={"request": request})
    return Response(
        {"message": "✅ Payment marked successfully", "shipment": serializer.data},
        status=status.HTTP_200_OK,
    )

###############################################


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def md_shipments(request):
    """
    List shipments where payment is marked but duty not approved yet
    """
    shipments = Shipment.objects.filter(
        payment_marked=True,
        duty_paid=False
    )
    serializer = MDShipmentSerializer(shipments, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_duty_paid(request, shipment_id):
    try:
        shipment = Shipment.objects.get(id=shipment_id)
        if not shipment.payment_marked:
            return Response({"error": "Payment not marked yet"}, status=400)

        shipment.duty_paid = True
        shipment.duty_paid_date = timezone.now() 

        shipment.duty_paid_reject = False
        shipment.md_reject_reason = None
        shipment.md_rejected_at = None
        shipment.save()

        # ShipmentPhase creation
        phase_master = ShipmentPhaseMaster.objects.get(id=6)
        ShipmentPhase.objects.update_or_create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )

        serializer = MDShipmentSerializer(shipment)
        return Response({"message": "Duty approved successfully", "shipment": serializer.data})

    except ShipmentPhaseMaster.DoesNotExist:
        return Response({"warning": "Phase master with ID 6 not found. Duty approved anyway."}, status=200)

    except Exception as e:
        # Print the actual error
        print("ERROR IN APPROVE DUTY:", e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


#################### Duty paid rejection

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_duty_paid(request, shipment_id):
    try:
        shipment = Shipment.objects.get(id=shipment_id)

        if not shipment.payment_marked:
            return Response(
                {"error": "Payment not marked yet"},
                status=status.HTTP_400_BAD_REQUEST
            )

        reason = request.data.get("reason", "").strip()
        if not reason:
            return Response(
                {"error": "Rejection reason is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- Reject logic ---
        shipment.duty_paid = False
        shipment.duty_paid_reject = True
        shipment.md_reject_reason = reason
        shipment.md_rejected_at = timezone.now()

        # Rollback payment step (send back to Bank Manager)
        shipment.payment_marked = False
        shipment.payment_marked_date = None

        shipment.save()

        serializer = MDShipmentSerializer(shipment)
        return Response(
            {
                "message": "Duty rejected successfully",
                "shipment": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    except Shipment.DoesNotExist:
        return Response(
            {"error": "Shipment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as e:
        print("ERROR IN REJECT DUTY:", e)
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )



################### Bank ###############

from .models import Bank
from .forms import BankForm


# List View
class BankListView(ListView):
    model = Bank
    template_name = 'masters/bank_list.html'
    context_object_name = 'banks'


# Create View
class BankCreateView(CreateView):
    model = Bank
    form_class = BankForm
    template_name = 'masters/bank_form.html'
    success_url = reverse_lazy('bank_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Update View
class BankUpdateView(UpdateView):
    model = Bank
    form_class = BankForm
    template_name = 'masters/bank_form.html'
    success_url = reverse_lazy('bank_list')


# Delete View
class BankDeleteView(DeleteView):
    model = Bank
    template_name = 'masters/bank_confirm_delete.html'
    success_url = reverse_lazy('bank_list')

################### END of BANK


#################### API




from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




#####################
from .services import get_sales_dashboard_data
@login_required
def sales_dashboard(request):
    context = get_sales_dashboard_data()
    return render(request, "dash/sales_dashboard.html", context)



@login_required
def sales_dashboard_api(request):
    data = get_sales_dashboard_data()
    return JsonResponse({
        "total_active_shipments": data["total_active_shipments"],
        "new_shipment": data["new_shipment"],
        "goods_at_port": data["goods_at_port"],
        "on_the_way_shipment": data["on_the_way_shipment"],
        "grn": data["grn"],
        "completed_shipment": data["completed_shipment"],
    })


###################################################################################3


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from masters.models import Shipment, BankDocument
from django.db.models import Sum, Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank_dashboard(request):
    today = timezone.now().date()
    first_day = today.replace(day=1)

    # 1️⃣ Total shipments created this month
    total_shipments_month = Shipment.objects.filter(created_at__date__gte=first_day).count()

    # 2️⃣ Active shipments (not yet completed or cleared)
    active_shipments = Shipment.objects.filter(
        duty_paid=False, 
        send_to_clearing_agent=True
    ).count()

    # 3️⃣ Pending bank documents (not settled)
    pending_docs = BankDocument.objects.filter(settled=False).count()

    # 4️⃣ Completed shipments (fully cleared and duty paid)
    completed_shipments = Shipment.objects.filter(duty_paid=True).count()

    # 5️⃣ Total amount pending (sum of unsettled bank docs)
    total_amount_pending = (
        BankDocument.objects.filter(settled=False)
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    return Response({
        "total_shipments_month": total_shipments_month,
        "active_shipments": active_shipments,
        "pending_docs": pending_docs,
        "completed_shipments": completed_shipments,
        "total_amount_pending": f"{total_amount_pending:,.2f}",
    })


################# API Data Entry
def parse_date(date_str):
    """Parse date from string, return None if invalid."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None
    

from .services import create_arrival_notice, update_shipment_stage
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shipment_create_api(request):
    data = request.data

    try:
        stage = data.get('stage', 'arrival')

        # ===============================
        # STAGE 1: ARRIVAL NOTICE
        # ===============================
        if stage == 'arrival':

            shipment = create_arrival_notice(data, request.user)

            return Response({
                'success': True,
                'message': 'Arrival Notice created successfully',
                'shipment_id': shipment.id,
                'shipment_code': shipment.shipment_code,
            }, status=status.HTTP_201_CREATED)

        # ===============================
        # STAGE 2: SHIPMENT / BANK DOCS
        # ===============================
        elif stage == 'shipment':

            if not data.get('shipment_id'):
                return Response(
                    {'error': 'shipment_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            shipment = update_shipment_stage(data, request.user)

            return Response({
                'success': True,
                'message': 'Shipment stage updated successfully',
                'shipment_id': shipment.id,
                'shipment_code': shipment.shipment_code,
            }, status=status.HTTP_200_OK)

        else:
            return Response(
                {'error': 'Invalid stage value'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Shipment.DoesNotExist:
        return Response(
            {'error': 'Shipment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
###############################    PHASE DISPLAY   ################################

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Shipment, ShipmentPhase

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shipment_detail_api(request, shipment_id):
    try:
        # Helper functions
        format_date = lambda d, fmt="%Y-%m-%d": d.strftime(fmt) if d else None
        #format_datetime = lambda d, fmt="%Y-%m-%d %H:%M": d.strftime(fmt) if d else None
        def format_datetime(d, fmt="%Y-%m-%d %H:%M"):
            if not d:
                return None
            return timezone.localtime(d).strftime(fmt)


        shipment = Shipment.objects.get(id=shipment_id)

        # Master phases
        master_phases = ShipmentPhaseMaster.objects.all().order_by('order')

        # Completed shipment phases
        shipment_phases = ShipmentPhase.objects.filter(shipment=shipment)
        completed_map = {p.phase_name: p for p in shipment_phases}

        # Build full list of phases
        phases_data = []
        for master_phase in master_phases:
            matched = completed_map.get(master_phase.phase_name)
            phases_data.append({
                "id": master_phase.id,
                "title": master_phase.phase_name,
                "completed": bool(matched),
                "completed_at": format_datetime(matched.completed_at) if matched else None
            })

        # Shipment details
        shipment_data = {
            "shipment_code": shipment.shipment_code,
            "bl": shipment.bl,
            "vessel": shipment.vessel,
            "container": shipment.container,
            "amount": shipment.amount,
            "expected_arrival_date": format_date(shipment.expected_arrival_date),
            "supplier": shipment.supplier.supplier_name if shipment.supplier else None,
        }

        # Journey summary
        journey_summary = [
            {
                "phase_code": 0,
                "title": "Arrival Notice",
                "details": {
                    "Shipment Code": shipment.shipment_code,
                    "Vessel": shipment.vessel,
                    "BL": shipment.bl,
                    "Container": shipment.container,
                    "Expected Arrival": format_date(shipment.expected_arrival_date),
                }
            },
            {
                "phase_code": 1,
                "title": "Document Collected",
                "details": {
                    "Supplier Invoice": shipment.supplier_invoice,
                    "Amount $": shipment.amount,
                    "Supplier": shipment.supplier.supplier_name if shipment.supplier else None,
                    "Bank Name": shipment.bank.b_name if shipment.bank else None,
                    "Packing List Ref": shipment.packing_list_ref,
                    "Gross Weight": shipment.cbm,
                    "Bank Doc Type": shipment.bank_doc_type,
                    "Reference Number": shipment.reference_number,
                    "Payment Type": shipment.payment_type,
                }
            },
            {
                "phase_code": 2,
                "title": "Document Handover",
                "details": {
                    "Clearing Agent": shipment.clearing_agent.username if shipment.clearing_agent else None,
                    "Date & Time": format_datetime(shipment.C_Process_Initiated_date),
                }
            },
            {
                "phase_code": 3,
                "title": "Duty Assessment",
                "details": {
                    "Assessment Upload Date": format_datetime(shipment.assessment_uploaded_date),
                    "Total Duty LKR": shipment.total_duty_value,
                    "Assessment PDF": shipment.assessment_document.url if shipment.assessment_document else None,
                    "Clearing Agent": shipment.clearing_agent.username if shipment.clearing_agent else None,
                }
            },
            {
                "phase_code": 456,
                "title": "Payment Process",
                "details": {
                    "Payment Request Date": format_datetime(shipment.payment_marked_date),
                    "Payment Method": shipment.payment_type,
                    "Bank Name": shipment.bank.b_name if shipment.bank else None,
                    "Payment Ref ID": shipment.payref_document_ref,
                    "Payment Proof": shipment.payref_document.url if shipment.payref_document else None,
                    "MD Approval": "Approved" if shipment.duty_paid else "Pending",
                    "Payment Finalized Date": format_datetime(shipment.duty_paid_date),
                    "Proof Downloaded": format_datetime(shipment.C_Process_Initiated_date),
                }
            },
            {
                "phase_code": 7,
                "title": "Dispatch",
                "details": {
                    "Arrival at Warehouse": format_datetime(shipment.arrival_at_warehouse_date),
                    "Departure at Warehouse": format_datetime(shipment.departure_at_warehouse_date),
                    "Condition on Departure": "Good",
                }
            },
            {
                "phase_code": 8,
                "title": "GRN Process",
                "details": {
                    "GRN Uploaded": "Yes" if shipment.grn_upload_at_warehouse else "No",
                    "GRN Upload Date": format_datetime(shipment.grn_upload_at_warehouse_date),
                    "GRN Confirmed": "Yes" if shipment.grn_complete_at_warehouse else "No",
                    "GRN Confirm Date": format_datetime(shipment.grn_complete_at_warehouse_date),
                }
            },
        ]

        return Response({
            "shipment": shipment_data,
            "phases": phases_data,
            "journey_summary": journey_summary,
        })

    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=404)

###################################


# masters/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Bank, Company, ItemCategory, Warehouse,Supplier
from .serializers import BankSerializer, CompanySerializer, ItemCategorySerializer, SupplierSerializer,ClearingAgentSerializer,BankManagerpayrefSerializer,BankManagerpaySerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def banks_list(request):
    banks = Bank.objects.all()
    serializer = BankSerializer(banks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def companies_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def items_list(request):
    items = ItemCategory.objects.all()
    serializer = ItemCategorySerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def warehouses_list(request):
    warehouses = Warehouse.objects.all()
    serializer = WarehouseSerializer(warehouses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suppliers_list(request):
    suppliers = Supplier.objects.all()
    serializer = SupplierSerializer(suppliers, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clearing_agents_list(request):
    clearing_agents = ClearingAgent.objects.all()
    serializer = ClearingAgentSerializer(clearing_agents, many=True)
    return Response(serializer.data)



def choice_list(choices):
    return [{'value': value, 'label': label} for value, label in choices]

@api_view(['GET'])
def bank_doc_types(request):
    """
    Returns list of bank document types for shipments.
    """
    data = [{'value': value, 'label': label} for value, label in Shipment.BANK_DOC_TYPES]
    return Response(data)

@api_view(['GET'])
def shipment_types(request):
    return Response(choice_list(Shipment.SHIPMENT_TYPES))

@api_view(['GET'])
def incoterms(request):
    return Response(choice_list(Shipment.INCOTERMS))

@api_view(['GET'])
def transport_modes(request):
    return Response(choice_list(Shipment.TRANSPORT_MODES))


@api_view(['GET'])
def item_warehouse_options(request):
    """
    Returns list of all item-warehouse combinations.
    """
    data = []
    for item in ItemCategory.objects.prefetch_related('warehouses'):
        for wh in item.warehouses.all():
            data.append({
                'id': f"{item.pk}_{wh.pk}",
                'label': f"{item.item_name} — {wh.warehouse_name}"
            })
    return Response(data)


from .models import Shipment
from .serializers import ShipmentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank_controller_shipments(request):
    if not request.user.groups.filter(name="Bank Controller").exists():
        return Response({"detail": "Permission denied"}, status=403)
    
  
    shipments = Shipment.objects.filter(send_to_clearing_agent=False, ship_status=2)
    
    serializer = ShipmentSerializer(shipments, many=True)
    return Response(serializer.data)


#### ----------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bank_controller_update_shipment(request, shipment_id):
    if not request.user.groups.filter(name="Bank Controller").exists():
        return Response({"detail": "Permission denied"}, status=403)

    shipment = get_object_or_404(Shipment, id=shipment_id)
    serializer = ShipmentSerializer(shipment, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        
        # Send email notification
        subject = f"Shipment {shipment.id} Updated by Bank Controller"
        message = f"Shipment {shipment.id} updated by {request.user.username}"
        from_email = "damvict@gmail.com"
        recipient_list = ["damayanthi.caipl@gmail.com"]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print("Email failed:", e)
        
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



##############_-----------
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_handover(request, shipment_id):

    clearing_agent_id = request.data.get("clearing_agent_id")

    if not clearing_agent_id:
        return Response(
            {"error": "clearing_agent_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # ✅ USE auth_user, NOT ClearingAgent
        clearing_agent = User.objects.get(id=clearing_agent_id)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid clearing agent"},
            status=status.HTTP_404_NOT_FOUND
        )

    # ✅ Safety check (recommended)
    if not clearing_agent.groups.filter(id=4).exists():
        return Response(
            {"error": "Selected user is not a clearing agent"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response(
            {"error": "Shipment not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        shipment.clearing_agent = clearing_agent   # ✅ auth_user
        shipment.send_to_clearing_agent = True
        shipment.send_date = timezone.now()
        ship_status=3
        shipment.save()
        # ✅ Create ShipmentPhase record
        phase_master = ShipmentPhaseMaster.objects.get(id=3)
        ShipmentPhase.objects.update_or_create(
                shipment=shipment,
                phase_code=phase_master.phase_code,
                defaults={
                    "phase_name": phase_master.phase_name,
                    "completed": True,
                    "completed_at": timezone.now(),
                    "updated_by": request.user,
                    "order": phase_master.order,
                }
        )

        
        ############################################
        return Response(
            {"success": "Handover confirmed and phase recorded"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print("SAVE ERROR:", str(e))
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST

    )



##################### Bank Manager API
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Shipment
from .serializers import ShipmentSerializer

# GET all shipments for bank manager
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank_manager_shipments_initiate(request):
    shipments = Shipment.objects.filter(
        send_to_clearing_agent=True,
        payment_marked=False,
        c_ass_send=True
        
    )
    serializer = ShipmentSerializer(shipments, many=True)
    return Response(serializer.data)

# POST update shipment by bank manager
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bank_manager_update(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    
    send_date = request.data.get("send_date")
    payment_marked = request.data.get("payment_marked", False)
    
    shipment.send_date = send_date or None
    
    if payment_marked:
        shipment.payment_marked = True
        if not shipment.payment_marked_date:
            shipment.payment_marked_date = timezone.now().date()
    else:
        shipment.payment_marked = False
        shipment.payment_marked_date = None
    
    shipment.save()
    
    return Response({"success": True, "shipment_id": shipment.id})


#~~~~~~~~~~~~~ shipment List

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from masters.models import Shipment
from masters.serializers import ShipmentSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shipment_list(request):
    shipments = Shipment.objects.all().order_by('-id')
    serializer = ShipmentSerializer(shipments, many=True)
    return Response(serializer.data)


######## end of Bank Manager API



################## CA 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clearing_agent_dispatch(request):
    shipments = Shipment.objects.filter(
        C_Process_Initiated=True,
        C_Process_completed=False,
        clearing_agent=request.user
    )
    serializer = ShipmentSerializer(shipments, many=True)
    return Response(serializer.data)



############_-------------------------------

from rest_framework import generics, permissions
from .models import ShipmentDispatch
from .serializers import ShipmentDispatchSerializer

class ShipmentDispatchCreateView(generics.CreateAPIView):
    queryset = ShipmentDispatch.objects.all()
    serializer_class = ShipmentDispatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get shipment_id from URL
        shipment_id = self.kwargs.get("shipment_id")

        # Save ShipmentDispatch
        dispatch = serializer.save(
            created_by=self.request.user,
            shipment_id=shipment_id
        )

        # Automatically create a ShipmentPhase for handover
        try:
            # Replace '8' with the correct phase master ID for dispatch/handover
                phase_master = ShipmentPhaseMaster.objects.get(id=9)
                ShipmentPhase.objects.create(
                    shipment=dispatch.shipment,  # link to the shipment
                    phase_code=phase_master.phase_code,
                    phase_name=phase_master.phase_name,
                    completed=True,
                    completed_at=timezone.now(),
                    updated_by=self.request.user,
                    order=phase_master.order
                )
        except ShipmentPhaseMaster.DoesNotExist:
            # Optional: handle if phase master not found
            pass




        ############### Truck Arrivals




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def truck_arrivals(request):
    shipments = ShipmentDispatch.objects.filter(        
        truck_depature=False
    )
    serializer = ShipmentDispatchSerializer(shipments, many=True)
    return Response(serializer.data)







############_-------------------------------

from .models import ShipmentDispatch, Shipment



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_arrival(request, shipment_id):
    try:
        # Update ShipmentDispatch
        dispatch = ShipmentDispatch.objects.get(id=shipment_id)
        dispatch.truck_arrived = True
        dispatch.truck_arrived_date = timezone.now()
        dispatch.save()

        # Update Shipment - only departure fields
        shipment = dispatch.shipment  # assuming OneToOneField or ForeignKey
        shipment. arrival_at_warehouse = True
        shipment.arrival_at_warehouse_date = timezone.now()
        shipment.save(update_fields=['arrival_at_warehouse', 'arrival_at_warehouse_date'])

        # Record shipment phase
        phase_master = ShipmentPhaseMaster.objects.get(id=10)
        ShipmentPhase.objects.create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )

        return Response({'status': 'success', 'message': 'Arrival recorded successfully.'})
    except ShipmentDispatch.DoesNotExist:
        return Response({'status': 'error', 'message': 'Arrivals not found.'}, status=404)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_departure(request, shipment_id):
    try:
        # Update ShipmentDispatch
        dispatch = ShipmentDispatch.objects.get(id=shipment_id)
        dispatch.truck_depature = True
        dispatch.truck_depature_date = timezone.now()
        dispatch.save()

        # Update Shipment - only departure fields
        shipment = dispatch.shipment  # assuming OneToOneField or ForeignKey
        shipment.departure_at_warehouse = True
        shipment.departure_at_warehouse_date = timezone.now()
        shipment.save(update_fields=['departure_at_warehouse', 'departure_at_warehouse_date'])

        phase_master = ShipmentPhaseMaster.objects.get(id=11)
        ShipmentPhase.objects.create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )

        return Response({'status': 'success', 'message': 'Departure recorded successfully.'})
    except ShipmentDispatch.DoesNotExist:
        return Response({'status': 'error', 'message': 'ShipmentDispatch not found.'}, status=404)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def grn_record(request):
    shipments = Shipment.objects.filter(
        arrival_at_warehouse=True,
        grn_upload_at_warehouse=False
    ).select_related('dispatch')  # ✅ One-to-one join for performance

    serializer = ShipmentSerializer(shipments, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_grn_upload(request, shipment_id):
  
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

       
    ###shipment.grn_upload_at_warehouse = True
    #####shipment.grn_upload_at_warehouse_date = timezone.now()
 

   # Get values from request
    grn_number = request.data.get("grn_number", "")
    receiving_notes = request.data.get("receiving_notes", "")
    physical_stock_verified = request.data.get("physical_stock_verified", False)
    grn_uploaded = request.data.get("grn_uploaded", False)

       # Save to shipment
    ###shipment.grn_upload_at_warehouse = True
    ####shipment.grn_upload_at_warehouse_date = timezone.now()
    shipment.grn_number = grn_number
    shipment.receiving_notes = receiving_notes
    shipment.physical_stock_verified = physical_stock_verified
    shipment.grn_uploaded = grn_uploaded 

    if physical_stock_verified and grn_uploaded:
        shipment.grn_upload_at_warehouse = True
        shipment.grn_upload_at_warehouse_date = timezone.now()

    shipment.save()

    # ---- Create ShipmentPhase record for handover ----
    try:
        phase_master = ShipmentPhaseMaster.objects.get(id=12)  # adjust ID
        ShipmentPhase.objects.create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )
    except ShipmentPhaseMaster.DoesNotExist:
        # Optional: skip or log error if phase master not found
        pass

    serializer = ShipmentSerializer(shipment)
    return Response(
        {"message": "GRN Uploaded successfully", "shipment": serializer.data},
        status=status.HTTP_200_OK
    )


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def grn_confirm(request):
    shipments = Shipment.objects.filter(     
        grn_complete_at_warehouse=False,
        grn_upload_at_warehouse=True

    )
    serializer = ShipmentSerializer(shipments, many=True)
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_grn_confirm(request, shipment_id):
  
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

       
    shipment.grn_complete_at_warehouse = True
    shipment.grn_complete_at_warehouse_date = timezone.now()
    shipment.ship_status=13
    shipment.save()

    # ---- Create ShipmentPhase record for handover ----
    try:
        phase_master = ShipmentPhaseMaster.objects.get(id=13)  # adjust ID
        ShipmentPhase.objects.create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )
    except ShipmentPhaseMaster.DoesNotExist:
        # Optional: skip or log error if phase master not found
        pass

    serializer = ShipmentSerializer(shipment)
    return Response(
        {"message": "GRN Confirm successfully", "shipment": serializer.data},
        status=status.HTTP_200_OK
    )



############# dashboards API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clearing_agent_summary(request):
    # Optional: filter only the logged-in clearing agent’s shipments
    shipments = Shipment.objects.all()

    completed = shipments.filter(ship_status=13).count()
    active = shipments.filter(ship_status__lt=13).count()
    overdue = shipments.filter(
        ship_status__lt=13,
        expected_arrival_date__gt=F('C_Process_completed_date')
    ).count()

    return Response({
        "active": active,
        "completed": completed,
        "overdue": overdue
    })



###################### Dashboard KPI ########
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    user = request.user
    today = timezone.now().date()
    first_day = today.replace(day=1)

    # Common date filters
    current_month_filter = Q(order_date__month=today.month, order_date__year=today.year)

    # Common shipment stats
    total_shipments_month = Shipment.objects.filter(current_month_filter,ship_status__gt=1).count()
    completed_shipments = Shipment.objects.filter(ship_status=13).count()
    active_shipments = Shipment.objects.filter(ship_status__lt=13).count()
    ship_tobe_create=Shipment.objects.filter(ship_status=1).count()
    doc_tobe_handover=Shipment.objects.filter(ship_status=2,send_to_clearing_agent=0).count()
    pen_ass=Shipment.objects.filter(ship_status=2,send_to_clearing_agent=1,clearing_agent_id=request.user.id,  c_ass_send=False).count()
    init_clearing=Shipment.objects.filter(send_to_clearing_agent_payment=True,C_Process_Initiated=0,clearing_agent_id=request.user ).count() 
    ca_dispatch=Shipment.objects.filter(C_Process_Initiated=True,C_Process_completed=False,clearing_agent_id=request.user ).count() 
   

    init_payment=Shipment.objects.filter( send_to_clearing_agent=True, payment_marked=False,c_ass_send=True).count()
    upload_payment=Shipment.objects.filter( duty_paid=True, send_to_clearing_agent_payment=False).count()
    payment_app=Shipment.objects.filter(  payment_marked=True,duty_paid=False).count()    

       

    overdue_shipments = Shipment.objects.filter(
        expected_arrival_date__lt=today,
    ).exclude(ship_status=13).count()
  ### on_the_way_shipments = Shipment.objects.filter(C_Process_Initiated=False).count()

    # Clearance stats
    clearance_initiated = Shipment.objects.filter(
        C_Process_Initiated=True, C_Process_completed=False
    ).count()
    clearance_completed = Shipment.objects.filter(C_Process_completed=True).count()
    goods_at_port = Shipment.objects.filter(C_Process_Initiated=False).count()

    on_the_way_shipment = Shipment.objects.filter(
        C_Process_completed=True, arrival_at_warehouse=False
    ).count()

    # Bank data
    pending_bank_docs = Shipment.objects.filter(ship_status=1).count()
    total_amount_pending = (
        BankDocument.objects.filter(settled=False).aggregate(total=Sum('amount'))['total'] or 0
    )
    approved_duty_payments = Shipment.objects.filter(duty_paid=True).count()

    # GRN data

  
    pending_grn = Shipment.objects.filter(arrival_at_warehouse=True, grn_complete_at_warehouse=False).count()
    record_grn = Shipment.objects.filter(arrival_at_warehouse=True, grn_complete_at_warehouse=False,grn_upload_at_warehouse=False).count()
    confirm_grn = Shipment.objects.filter(grn_complete_at_warehouse=False,grn_upload_at_warehouse=True).count()

    
    
    total_grn_value_month = (
        Shipment.objects.filter(grn_complete_at_warehouse_date__month=today.month)
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    # Invoice data
    total_invoice_value = (
        Shipment.objects.aggregate(total=Sum('amount'))['total'] or 0
    )

    # Build metrics per user group
    data = {
        "common": {
            "total_shipments_month": total_shipments_month,
            "completed_shipments": completed_shipments,
            "active_shipments": active_shipments,
            "overdue_shipments": overdue_shipments,
            "on_the_way_shipment":on_the_way_shipment,
        }
    }

    if user.groups.filter(name="Bank Controller").exists():
        data["bank"] = {
            "pending_bank_docs": pending_bank_docs,
            "total_amount_pending": f"{total_amount_pending:,.2f}",
            "approved_duty_payments": approved_duty_payments,
            "pending_grn":pending_grn,
            "ship_tobe":ship_tobe_create,
            "doc_tobe_handover":doc_tobe_handover,
        }

    if user.groups.filter(name="Imports Department").exists():
        data["import"] = {
            "goods_at_port": goods_at_port,
            "clearance_initiated": clearance_initiated,
            "clearance_completed": clearance_completed,
            "pending_grn": pending_grn,
            "total_grn_value_month": f"{total_grn_value_month:,.2f}",
            "completed_shipments": completed_shipments,
             "total_invoice_value": f"{total_invoice_value:,.2f}",
             "approved_duty_payments": approved_duty_payments,
             "pending_bank_docs" : Shipment.objects.filter(ship_status=1).count(),
             "confirm_grn":confirm_grn,
             
        }

    if user.groups.filter(name="Bank Manager").exists():
        data["bm"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
            "init_payment": init_payment,
            "upload_payment": upload_payment,
        }

    if user.groups.filter(name="Clearing Agent").exists():
        data["ca"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
            "pen_ass":pen_ass,    
            "init_clearing": init_clearing, 
            "ca_dispatch": ca_dispatch
        }

    if user.groups.filter(name="Managing Director").exists():
        data["md"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
            "clearance_initiated": clearance_initiated,
            "clearance_completed": clearance_completed,
            "pending_grn":pending_grn,
            "total_grn_value_month":total_grn_value_month,
            "payment_app": payment_app,
            
        }   

    if user.groups.filter(name="Security Guard").exists():
        data["sg"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
            "on_the_way_shipment":on_the_way_shipment,
            "total_shipments_month":total_shipments_month,
        }

    if user.groups.filter(name="Warehouse Staff").exists():
        data["ws"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
            "record_grn":record_grn,
        }


    return Response(data)





################ shipment code
from django.db.models import Max
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_next_shipment_code(request):
    shipment_type = request.query_params.get("type", "IMP")
    year = timezone.now().year
    prefix = shipment_type or "IMP"

    last_seq = (
        Shipment.objects
        .filter(shipment_type=shipment_type, shipment_code__startswith=f"{prefix}-{year}-")
        .aggregate(max_seq=Max("shipment_sequence"))["max_seq"] or 0
    )
    next_seq = last_seq + 1
    next_code = f"{prefix}-{year}-{next_seq:03d}"

    return Response({"next_code": next_code})





####################### Settlements
# -------------------------------
# BANK DOCUMENT ENDPOINTS
# -------------------------------


@api_view(['GET', 'POST'])
def bank_documents_list(request):
    """List all bank documents or create a new one."""
    if request.method == 'GET':
        docs = BankDocument.objects.all()
        result = []

        for doc in docs:
            # Calculate total settled amount
            total_settled = Settlement.objects.filter(document=doc).aggregate(total=models.Sum('amount'))['total'] or 0
            doc_data = BankDocumentSerializer(doc).data
            doc_data['balance'] = float(doc.amount or 0) - float(total_settled)  # compute balance
            result.append(doc_data)

        return Response(result)

    elif request.method == 'POST':
        serializer = BankDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def bank_document_detail(request, pk):
    """Retrieve, update, or delete a specific bank document."""
    try:
        doc = BankDocument.objects.get(pk=pk)
    except BankDocument.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BankDocumentSerializer(doc)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BankDocumentSerializer(doc, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------
# SETTLEMENT ENDPOINTS
# -------------------------------
from .models import BankDocument, Settlement
from .serializers import BankDocumentSerializer, SettlementSerializer



@api_view(['GET', 'POST'])
def settlements_list(request):
    if request.method == 'GET':
        settlements = Settlement.objects.select_related('document').all()
        serializer = SettlementSerializer(settlements, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SettlementSerializer(data=request.data)
        if serializer.is_valid():
            settlement = serializer.save()

            # Only create a new IMP BankDocument if settlement_type is IMP
            if settlement.settlement_type == 'IMP':
                # Create a new BankDocument for this IMP settlement
                BankDocument.objects.create(
                    shipment=settlement.document.shipment if settlement.document else None,
                    doc_type='IMP',
                    reference_number=settlement.reference_number,
                    amount=settlement.amount,
                    issue_date=timezone.now().date(),
                    due_date=timezone.now().date(),
                    bank=settlement.document.bank if settlement.document else None,
                    company=settlement.document.company if settlement.document else None,
                    created_by=settlement.document.created_by if settlement.document else None,
                    settlement_date=settlement.settlement_date,
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def settlement_detail(request, pk):
    """Retrieve, update, or delete a specific settlement record."""
    try:
        settlement = Settlement.objects.get(pk=pk)
    except Settlement.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SettlementSerializer(settlement)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SettlementSerializer(settlement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        settlement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


################# Bank balances display
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Q, F
from .models import Bank, BankDocument, Settlement

@api_view(['GET'])
def bank_documents_summary(request):
    """
    Display each bank with OD/LC/IMP/DA values
    and show current balance of LC/DA/IMP from settlements.
    """
    banks = Bank.objects.all()
    result = []

    for bank in banks:
        # Base data from the bank table
        bank_data = {
            "bank_name": bank.b_name,
            "accno": bank.accno,
            "branch": bank.branch,
            "od": float(bank.od or 0),
            "lc": float(bank.lc or 0),
            "imp": float(bank.imp or 0),
            "da": float(bank.da or 0),
        }

        # For each doc type (LC, DA, IMP) calculate total outstanding balance
        balances = {}
        for doc_type in ["LC", "DA", "IMP"]:
            total_doc_amount = (
                BankDocument.objects.filter(bank=bank, doc_type=doc_type)
                .aggregate(total=Sum("amount"))["total"] or 0
            )

            total_settled = (
                Settlement.objects.filter(document__bank=bank, document__doc_type=doc_type)
                .aggregate(total=Sum("amount"))["total"] or 0
            )

            balances[doc_type] = float(total_doc_amount) - float(total_settled)

        bank_data["current_balances"] = balances
        result.append(bank_data)

    return Response(result)



############## OS Repprt ###############

from django.db.models import Sum
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def outstanding_report(request):

    as_at = parse_date(request.GET.get("date"))
    company_id = request.GET.get("company_id")
    doc_type = request.GET.get("doc_type")

    documents = BankDocument.objects.select_related(
        "company", "bank"
    ).prefetch_related("settlements")

    if company_id:
        documents = documents.filter(company_id=company_id)

    if doc_type and doc_type != "ALL":
        documents = documents.filter(doc_type=doc_type)

    results = []

    for doc in documents:
        settled_amount = (
            doc.settlements
            .filter(settlement_date__lte=as_at)
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        balance = (doc.amount or 0) - settled_amount

        if balance > 0:
            results.append({
                "id": doc.id,
                "company": doc.company.name if doc.company else "",
                "doc_type": doc.doc_type,
                "reference_number": doc.reference_number,
                "issue_date": doc.issue_date,
                "due_date": doc.due_date,
                "amount": float(doc.amount or 0),
                "balance": float(balance),
            })

    return Response(results)



############# OS - Excel


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def outstanding_export_excel(request):
    date_str = request.GET.get("date")
    company_id = request.GET.get("company_id")
    doc_type = request.GET.get("doc_type", "ALL")

    if not date_str:
        return Response(
            {"error": "date parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    as_at_date = parse_date(date_str)

    data = get_outstanding_data(company_id, doc_type, as_at_date)

    wb = Workbook()
    ws = wb.active
    ws.title = "Outstanding Report"

    ws.append([
        "Company",
        "Doc Type",
        "Reference",
        "Issue Date",
        "Amount",
        "Outstanding"
    ])

    for d in data:
        ws.append([
            d["company"],
            d["doc_type"],
            d["reference_number"],
            d["issue_date"],
            d["amount"],
            d["balance"],
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="Outstanding_{as_at_date}.xlsx"'
    )

    wb.save(response)
    return response



################### Cleqaring Agents

from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ClearingAgentUserSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def clearing_agent_users(request):
    users = User.objects.filter(
        groups__id=4,   # ✅ DIRECT & SAFE
        is_active=True
    ).order_by("first_name", "username")

    serializer = ClearingAgentUserSerializer(users, many=True)
    return Response(serializer.data)





################## REPORTS EXPORT
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def outstanding_report_email(request):
    user = request.user

    company_id = request.data.get("company_id")
    doc_type = request.data.get("doc_type", "ALL")
    date_str = request.data.get("date")
    format = request.data.get("format")

    if not date_str or format not in ["excel", "pdf"]:
        return Response(
            {"error": "Invalid parameters"},
            status=status.HTTP_400_BAD_REQUEST
        )

    as_at_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    qs = get_outstanding_queryset(company_id, doc_type, as_at_date)

    if format == "excel":
        buffer = generate_outstanding_excel(qs, as_at_date)
        filename = "Outstanding_Report.xlsx"
    else:
        buffer = generate_outstanding_pdf(qs, as_at_date)
        filename = "Outstanding_Report.pdf"

    send_report_email(user, buffer, filename)

    return Response(
        {"success": f"{format.upper()} report emailed successfully"},
        status=status.HTTP_200_OK
    )



##########////
from django.db.models import Sum
from datetime import datetime
from io import BytesIO

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

#from models import BankDocument, Settlement


def get_outstanding_queryset(company_id=None, doc_type=None, as_at_date=None):
    qs = BankDocument.objects.all()

    if company_id:
        qs = qs.filter(company_id=company_id)

    if doc_type and doc_type != "ALL":
        qs = qs.filter(doc_type=doc_type)

    if as_at_date:
        qs = qs.filter(issue_date__lte=as_at_date)

    return qs


def calculate_balance(document, as_at_date):
    settled = (
        document.settlements
        .filter(settlement_date__lte=as_at_date)
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    return float(document.amount or 0) - float(settled)


def generate_outstanding_excel(qs, as_at_date):
    wb = Workbook()
    ws = wb.active
    ws.title = "Outstanding Report"

    ws.append([
        "Company",
        "Doc Type",
        "Reference",
        "Issue Date",
        "Amount",
        "Outstanding Balance"
    ])

    for doc in qs:
        balance = calculate_balance(doc, as_at_date)
        if balance <= 0:
            continue

        ws.append([
            doc.company.name if doc.company else "",
            doc.doc_type,
            doc.reference_number,
            doc.issue_date.strftime("%Y-%m-%d"),
            float(doc.amount or 0),
            balance
        ])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


def generate_outstanding_pdf(qs, as_at_date):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, f"Outstanding Report as at {as_at_date}")
    y -= 30

    pdf.setFont("Helvetica", 10)

    for doc in qs:
        balance = calculate_balance(doc, as_at_date)
        if balance <= 0:
            continue

        text = (
            f"{doc.company.name if doc.company else ''} | "
            f"{doc.doc_type} | "
            f"{doc.reference_number} | "
            f"Balance: {balance:,.2f}"
        )

        pdf.drawString(40, y, text)
        y -= 18

        if y < 50:
            pdf.showPage()
            y = height - 40

    pdf.save()
    buffer.seek(0)
    return buffer


from django.core.mail import EmailMessage
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

def send_report_email(user, file_buffer, filename):
    try:
        email = EmailMessage(
            subject="Outstanding Report",
            body="Please find attached the Outstanding Report.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        email.attach(
            filename,
            file_buffer.read(),
            "application/octet-stream"
        )

        email.send(fail_silently=False)
        logger.info(f"📧 Outstanding report email sent to {user.email}")

    except Exception as e:
        logger.error(f"❌ Email sending failed: {str(e)}")
        raise


def get_outstanding_data(company_id=None, doc_type=None, as_at_date=None):
    documents = BankDocument.objects.select_related(
        "company", "bank"
    ).prefetch_related("settlements")

    if company_id:
        documents = documents.filter(company_id=company_id)

    if doc_type and doc_type != "ALL":
        documents = documents.filter(doc_type=doc_type)

    results = []

    for doc in documents:
        settled_amount = (
            doc.settlements
            .filter(settlement_date__lte=as_at_date)
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        balance = (doc.amount or 0) - settled_amount

        if balance > 0:
            results.append({
                "company": doc.company.name if doc.company else "",
                "doc_type": doc.doc_type,
                "reference_number": doc.reference_number,
                "issue_date": doc.issue_date,
                "amount": float(doc.amount or 0),
                "balance": float(balance),
            })

    return results




########## ~~~~~~~~~~~~~~~~~~~~~~~~~ WEB FIXES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

################# BC ############

@login_required
def bank_controller_dashboard_web(request):
    user = request.user
    today = timezone.now().date()

    # ---------------- KPIs ----------------
    current_month_filter = Q(
        order_date__month=today.month,
        order_date__year=today.year
    )

    total_shipments_month = Shipment.objects.filter(
        current_month_filter, ship_status__gt=1
    ).count()

    active_shipments = Shipment.objects.filter(ship_status__lt=13).count()
    completed_shipments = Shipment.objects.filter(ship_status=13).count()

    pending_bank_docs = Shipment.objects.filter(ship_status=1).count()

    total_amount_pending = (
        BankDocument.objects.filter(settled=False)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    ship_tobe = Shipment.objects.filter(ship_status=1).count()
    doc_tobe_handover = Shipment.objects.filter(
        ship_status=2, send_to_clearing_agent=False
    ).count()

    context = {
        "stats": {
            "total_shipments_month": total_shipments_month,
            "active_shipments": active_shipments,
            "completed_shipments": completed_shipments,
            "pending_bank_docs": pending_bank_docs,
            "total_amount_pending": f"{total_amount_pending:,.2f}",
            "ship_tobe": ship_tobe,
            "doc_tobe_handover": doc_tobe_handover,
        }
    }

    return render(
        request,
        "bc/bank_controller_dashboard_web.html",
        context
    )



################# CL 
from django.views.decorators.cache import never_cache
@login_required
@never_cache
def clearing_agent_dashboard(request):
    if not request.user.groups.filter(name="Clearing Agent").exists():
        return render(request, "dashboard/access_denied.html")

    ca = request.user

    stats = {   # ✅ NO extra nesting
        "pen_ass": Shipment.objects.filter(
            clearing_agent=ca,
            send_to_clearing_agent=True,
            c_ass_send=False,
            ship_status=3
        ).count(),

        "init_clearing": Shipment.objects.filter(
            clearing_agent=ca,
            send_to_clearing_agent_payment=True,
            C_Process_Initiated=False
        ).count(),

        "ca_dispatch": Shipment.objects.filter(
            clearing_agent=ca,
            C_Process_Initiated=True,
            C_Process_completed=False
        ).count(),
    }

    return render(
        request,
        "dash/clearing_agent_dashboard.html",
        {"stats": stats}
    )








@login_required
def bank_controller_shipments_web(request):
    # 🔐 Permission check
    #if not request.user.groups.filter(name="Bank Controller").exists():
        #return redirect("admin_dashboard")  # or return HttpResponseForbidden()

    shipments = Shipment.objects.filter(
        send_to_clearing_agent=False,
        ship_status=2,
        
    )

    return render(
        request,
        "shipments/document_handover.html",
        {"shipments": shipments}
    )


@login_required
def clearing_agent_users_web(request):
    users = User.objects.filter(
        groups__id=4,        # Clearing Agent group
        is_active=True
    ).order_by("first_name", "username")

    data = [
        {
            "id": u.id,
            "username": u.username,
            "display_name": f"{u.first_name} {u.last_name}".strip() or u.username
        }
        for u in users
    ]

    return JsonResponse(data, safe=False)





@login_required
def confirm_handover_web(request, shipment_id):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request method"},
            status=405
        )

    try:
        data = json.loads(request.body)
        clearing_agent_id = data.get("clearing_agent_id")
    
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    if not clearing_agent_id:
        return JsonResponse(
            {"error": "clearing_agent_id is required"},
            status=400
        )

    # ✅ Get clearing agent (auth user)
    try:
        clearing_agent = User.objects.get(id=clearing_agent_id)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "Invalid clearing agent"},
            status=404
        )

    # ✅ Ensure user is a clearing agent
    if not clearing_agent.groups.filter(id=4).exists():
        return JsonResponse(
            {"error": "Selected user is not a clearing agent"},
            status=400
        )

    # ✅ Get shipment
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return JsonResponse(
            {"error": "Shipment not found"},
            status=404
        )

    try:
        shipment.clearing_agent = clearing_agent
        shipment.send_to_clearing_agent = True
        shipment.send_date = timezone.now()
        shipment.ship_status = 3   # ✅ FIXED
        shipment.ship_arival_date=timezone.now() + timedelta(days=3)
        shipment.save()

        # ✅ Record phase
        phase_master = ShipmentPhaseMaster.objects.get(id=3)
        ShipmentPhase.objects.update_or_create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            defaults={
                "phase_name": phase_master.phase_name,
                "completed": True,
                "completed_at": timezone.now(),
                "updated_by": request.user,
                "order": phase_master.order,
            }
        )

        return JsonResponse(
            {"success": "Handover confirmed and phase recorded"},
            status=200
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=400
        )
    


    ############################################## CL ~~~~~~~~~~~~~~~
@login_required
def clearing_agent_shipments_web(request):
    # 🔐 Role safety (recommended)
    if not request.user.groups.filter(name="Clearing Agent").exists():
        return render(request, "dashboard/access_denied.html")

    shipments = Shipment.objects.filter(
        clearing_agent=request.user,
        send_to_clearing_agent=True
    ).filter(
        Q(assessment_document__isnull=True) | Q(assessment_document='')
    )

    return render(
        request,
        "masters/clearing_agent_shipments.html",
        {"shipments": shipments}
    )


#~~~~~~~~~~~~~~~



from .models import Shipment


@login_required
def ca_pending_assessment_web(request):
    # 🔐 Only Clearing Agent
    if not request.user.groups.filter(name="Clearing Agent").exists():
        return render(request, "dashboard/access_denied.html")

    # GET → show list
    if request.method == "GET":
        shipments = Shipment.objects.filter(
            send_to_clearing_agent=True,
            c_ass_send=0,
            clearing_agent=request.user,
           
        ).select_related("supplier")

        return render(
            request,
            "dash/ca_pending_assessment.html",
            {"shipments": shipments},
        )

    # POST → upload assessment
    shipment_id = request.POST.get("shipment_id")
    total_duty = request.POST.get("total_duty_value")
    file = request.FILES.get("assessment_document")

    shipment = get_object_or_404(
        Shipment,
        id=shipment_id,
        clearing_agent=request.user,   # 🔐 security
    )

    # ❌ File is mandatory (same as API)
    if not file:
        messages.error(request, "Assessment document is mandatory.")
        return redirect("ca_pending_assessment")

    # ✅ Create phase (same logic as API)
    try:
        phase_master = ShipmentPhaseMaster.objects.get(id=4)
        ShipmentPhase.objects.get_or_create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            defaults={
                "phase_name": phase_master.phase_name,
                "completed": True,
                "completed_at": timezone.now(),
                "updated_by": request.user,
                "order": phase_master.order,
            },
        )
    except ShipmentPhaseMaster.DoesNotExist:
        messages.error(request, "Phase master not found.")
        return redirect("ca_pending_assessment")

    # ✅ Save assessment (same as API)
    shipment.assessment_document = file
    shipment.total_duty_value = total_duty
    shipment.assessment_uploaded_date = timezone.now()
    shipment.c_ass_send = True
    shipment.save()

    messages.success(request, "Assessment uploaded successfully.")
    ###return redirect("ca_pending_assessment")
    return redirect("clearing_agent_dashboard")



################# Bank Manager

def is_bank_manager(user):
    return user.groups.filter(name="Bank Manager").exists()

@login_required
@user_passes_test(is_bank_manager)
def bank_manager_dashboard(request):
    init_payment = Shipment.objects.filter(
        send_to_clearing_agent=True,
        payment_marked=False,
        c_ass_send=True
    ).count()

    upload_payment = Shipment.objects.filter(
        duty_paid=True,
        send_to_clearing_agent_payment=False
    ).count()

    context = {
        "bm": {
            "init_payment": init_payment,
            "upload_payment": upload_payment,
        }
    }

    return render(
        request,
        "dash/bank_manager_dashboard.html",
        context
    )






@login_required
@user_passes_test(is_bank_manager)
def bank_manager_initiate_payment(request):
    shipments = Shipment.objects.filter(
        send_to_clearing_agent=True,
        payment_marked=False,
        c_ass_send=True
    ).order_by("-id")

    return render(
        request,
        "dash/bank_manager_initiate_payment.html",
        {"shipments": shipments}
    )


@login_required
@user_passes_test(is_bank_manager)
def bank_manager_mark_payment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    shipment.payment_marked = True
    shipment.payment_marked_date = timezone.now().date()
    shipment.save()

    return redirect("bank_manager_initiate_payment")



def is_bank_manager(user):
    return user.groups.filter(name="Bank Manager").exists()


@login_required
@user_passes_test(is_bank_manager)
def bank_manager_payment_details(request, shipment_id):
    print("BANK MANAGER PAYMENT DETAILS VIEW HIT:", shipment_id)
    shipment = get_object_or_404(Shipment, id=shipment_id)
    banks = Bank.objects.all().order_by("b_name")
    
    return render(
        request,
        "dash/bank_manager_payment_details.html",
        {
            "shipment": shipment,
            "banks": banks,
        }
    )





@login_required
@user_passes_test(is_bank_manager)
def bank_manager_submit_payment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == "POST":
        payment_type = request.POST.get("payment_type")
        duty_paid_bank = request.POST.get("duty_paid_bank")
        pay_note = request.POST.get("notes")
        
        if not payment_type:
            messages.error(request, "Please select a payment method.")
            return redirect("bank_manager_payment_details", shipment_id=shipment.id)

        if not duty_paid_bank:
            messages.error(request, "Please select a bank.")
            return redirect("bank_manager_payment_details", shipment_id=shipment.id)
        
        # Map payment type (same logic as mobile)
        shipment.payment_type = payment_type
        shipment.duty_paid_bank = duty_paid_bank
        shipment.pay_note = pay_note
        shipment.payment_marked = True
        shipment.payment_marked_date = timezone.now()
        shipment.save()
        messages.success(request, "Payment details sent for MD approval.")
        return redirect("bank_manager_initiate_payment")

    return redirect("bank_manager_payment_details", shipment_id=shipment.id)



@login_required
@user_passes_test(is_bank_manager)
def bank_manager_send_md_approval(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == "POST":
        duty_paid_bank = request.POST.get("duty_paid_bank")
        payment_type = request.POST.get("payment_type")
        pay_note = request.POST.get("pay_note")

        # Update payment info
        if duty_paid_bank:
            shipment.duty_paid_bank = duty_paid_bank

        if payment_type in dict(Shipment.PAYMENT_TYPES):
            shipment.payment_type = payment_type

        if pay_note:
            shipment.pay_note = pay_note

        # Mark payment done
        shipment.payment_marked = True
        shipment.payment_marked_date = timezone.now()
        shipment.save()

        # ---- Create ShipmentPhase record ----
        try:
            phase_master = ShipmentPhaseMaster.objects.get(id=5)  # MD Approval phase
            ShipmentPhase.objects.create(
                shipment=shipment,
                phase_code=phase_master.phase_code,
                phase_name=phase_master.phase_name,
                completed=True,
                completed_at=timezone.now(),
                updated_by=request.user,
                order=phase_master.order,
            )
        except ShipmentPhaseMaster.DoesNotExist:
            pass

        # ---- SEND EMAIL TO MD ----
        subject = f"MD Approval Required – Shipment {shipment.shipment_code}"

        message = f"""
Dear Sir,

The Bank Manager has submitted payment details for MD approval.

Shipment Code     : {shipment.shipment_code}
Supplier Invoice  : {shipment.supplier_invoice or 'N/A'}
Reference Number  : {shipment.reference_number or 'N/A'}
Total Duty Value  : LKR {shipment.total_duty_value or 'N/A'}

Payment Method    : {shipment.get_payment_type_display()}
Duty Paid Bank    : {shipment.duty_paid_bank}

Notes:
{shipment.pay_note or 'No notes provided'}

Submitted by:
{request.user.get_full_name() or request.user.username}

Please review and proceed with approval.

Regards,
ISWM System
"""

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.MD_EMAIL],
                cc=["damayanthi@anuragroup.lk"],
                fail_silently=False,
            )
        except Exception as e:
            print("MD EMAIL ERROR:", e)

        return redirect("bank_manager_view")

    return redirect("bank_manager_payment_details", shipment_id=shipment.id)




####################### MD Web    ######################################




@login_required
def md_payment_approvals(request):
    shipments = Shipment.objects.filter(
        payment_marked=True,
        duty_paid=False
    ).order_by("-payment_marked_date")

    return render(request, "md/payment_approvals.html", {
        "shipments": shipments
    })



@login_required
def md_approve_web(request, shipment_id):
    if request.method == "POST":
        shipment = get_object_or_404(Shipment, id=shipment_id)

        shipment.duty_paid = True
        shipment.duty_paid_date = timezone.now()
        shipment.duty_paid_reject = False
        shipment.md_reject_reason = None
        shipment.md_rejected_at = None
        shipment.save()

        phase_master = ShipmentPhaseMaster.objects.get(id=6)
        ShipmentPhase.objects.update_or_create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )

    return redirect("md-payment-approvals")


# masters/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Shipment

@login_required
def bank_manager_payment_references_web(request):
    shipments = Shipment.objects.filter(
        duty_paid=True,
        send_to_clearing_agent_payment=False
    ).order_by("-duty_paid_date")

    return render(
        request,
        "bank_manager/payment_reference_list.html",
        {"shipments": shipments}
    )


@login_required
def bank_manager_payment_reference_detail_web(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == "POST":
        payref_document_ref = request.POST.get("payref_document_ref")
        file = request.FILES.get("payref_document")

        # 🔴 Validation (same as API)
        if not payref_document_ref:
            messages.error(request, "Payment reference is required.")
            return redirect(request.path)

        # 🔴 File size validation (10MB)
        if file and file.size > 10 * 1024 * 1024:
            messages.error(request, "File too large (max 10MB).")
            return redirect(request.path)

        # 🔴 Delete old file if exists
        if (
            file and shipment.payref_document
            and hasattr(shipment.payref_document, "path")
            and os.path.isfile(shipment.payref_document.path)
        ):
            os.remove(shipment.payref_document.path)

        # 🔴 Assign values (same fields as API)
        if file:
            shipment.payref_document = file

        shipment.payref_document_ref = payref_document_ref
        shipment.send_to_clearing_agent_payment = True
        shipment.send_to_clearing_agent_payment_date = timezone.now()

        # 🔴 Atomic save + phase creation
        try:
            with transaction.atomic():
                shipment.save()

                try:
                    phase_master = ShipmentPhaseMaster.objects.get(id=7)
                    ShipmentPhase.objects.create(
                        shipment=shipment,
                        phase_code=phase_master.phase_code,
                        phase_name=phase_master.phase_name,
                        completed=True,
                        completed_at=timezone.now(),
                        updated_by=request.user,
                        order=phase_master.order,
                    )
                except ShipmentPhaseMaster.DoesNotExist:
                    pass

            messages.success(request, "✅ Payment marked successfully.")
            return redirect("bank-manager-payment-references")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect(request.path)

    return render(
        request,
        "bank_manager/payment_reference_detail.html",
        {"shipment": shipment}
    )


@login_required
def initiate_clearing_web(request):
    shipments = Shipment.objects.filter(
        send_to_clearing_agent_payment=True,
        clearing_agent=request.user,
        C_Process_Initiated=False
      ).select_related("supplier").order_by("duty_paid_date")

         
    return render(
        request,
        "clearing_agent/initiate_clearing_list.html",
        {"shipments": shipments}
    )




@login_required
def initiate_clearing_submit_web(request, shipment_id):
    if request.method == "POST":
        shipment = get_object_or_404(
            Shipment,
            id=shipment_id,
            clearing_agent=request.user
        )

        shipment.C_Process_Initiated = True
        shipment.C_Process_Initiated_date = timezone.now()
        shipment.save()

        try:
            phase_master = ShipmentPhaseMaster.objects.get(id=8)
            ShipmentPhase.objects.create(
                shipment=shipment,
                phase_code=phase_master.phase_code,
                phase_name=phase_master.phase_name,
                completed=True,
                completed_at=timezone.now(),
                updated_by=request.user,
                order=phase_master.order,
            )
        except ShipmentPhaseMaster.DoesNotExist:
            pass

    return redirect("initiate-clearing-web")


@login_required
def clearing_agent_dispatch_web(request):
    # 🔐 Role safety
    if not request.user.groups.filter(name="Clearing Agent").exists():
        return render(request, "dashboard/access_denied.html")

    shipments = Shipment.objects.filter(
        C_Process_Initiated=True,
        C_Process_completed=False,
        clearing_agent=request.user   
    ).select_related("supplier").order_by("-C_Process_Initiated_date")

    return render(
        request,
        "clearing_agent/dispatch_list.html",
        {"shipments": shipments}
    )


@login_required
def clearing_agent_dispatch_detail_web(request, shipment_id):
    # 🔐 Role safety
    if not request.user.groups.filter(name="Clearing Agent").exists():
        return render(request, "dashboard/access_denied.html")

    shipment = get_object_or_404(
        Shipment,
        id=shipment_id,
        clearing_agent=request.user,
        C_Process_Initiated=True,
        C_Process_completed=False
    )

    # ---------------- POST (Save Dispatch) ----------------
    if request.method == "POST":

        dispatch = ShipmentDispatch.objects.create(
            shipment=shipment,
            truck_no=request.POST.get("truck_no"),
            driver_name=request.POST.get("driver_name"),
            driver_license=request.POST.get("driver_license"),
            driver_phone=request.POST.get("driver_phone"),
            transport_company=request.POST.get("transport_company"),
            estimated_delivery=request.POST.get("estimated_delivery"),
            delivery_address=request.POST.get("delivery_address"),
            special_instructions=request.POST.get("special_instructions"),
            created_by=request.user,
        )

            # ✅ UPDATE SHIPMENT DISPATCH STATUS
        shipment.ship_dispatch = True
        shipment.ship_dispatch_date = timezone.now()
        shipment.save(update_fields=["ship_dispatch", "ship_dispatch_date"])

        # Create shipment phase (same as API)
        try:
            phase_master = ShipmentPhaseMaster.objects.get(id=9)
            ShipmentPhase.objects.create(
                shipment=shipment,
                phase_code=phase_master.phase_code,
                phase_name=phase_master.phase_name,
                completed=True,
                completed_at=timezone.now(),
                updated_by=request.user,
                order=phase_master.order,
            )
        except ShipmentPhaseMaster.DoesNotExist:
            pass

        messages.success(request, "Shipment dispatched successfully.")
        return redirect("clearing-agent-dispatch-web")

    # ---------------- GET (Show Form) ----------------
    return render(
        request,
        "clearing_agent/dispatch_detail.html",
        {"shipment": shipment}
    )



###################### Security Guard Wev Views ########################

@login_required
def sg_dashboard_web(request):

    if not request.user.groups.filter(name="Security Guard").exists():
        return render(request, "dashboard/access_denied.html")

    on_the_way_shipment = Shipment.objects.filter(
        C_Process_completed=True,
        arrival_at_warehouse=False
    ).count()

    print("SG DASHBOARD | on_the_way_shipment =", on_the_way_shipment)

    return render(
        request,
        "security_guard/dashboard.html",
        {"on_the_way_shipment": on_the_way_shipment}
    )



@login_required
def truck_arrivals_web(request):
    shipments = ShipmentDispatch.objects.filter(
        truck_depature=False
    ).select_related("shipment")

    return render(
        request,
        "security_guard/truck_arrivals.html",
        {"shipments": shipments}
    )

@login_required
def record_arrival_web(request, dispatch_id):
    dispatch = get_object_or_404(ShipmentDispatch, id=dispatch_id)

    dispatch.truck_arrived = True
    dispatch.truck_arrived_date = timezone.now()
    dispatch.save()

    shipment = dispatch.shipment
    shipment.arrival_at_warehouse = True
    shipment.arrival_at_warehouse_date = timezone.now()
    shipment.save(update_fields=[
        "arrival_at_warehouse",
        "arrival_at_warehouse_date"
    ])

    phase_master = ShipmentPhaseMaster.objects.get(id=10)
    ShipmentPhase.objects.create(
        shipment=shipment,
        phase_code=phase_master.phase_code,
        phase_name=phase_master.phase_name,
        completed=True,
        completed_at=timezone.now(),
        updated_by=request.user,
        order=phase_master.order,
    )

    messages.success(request, "Arrival recorded successfully.")
    return redirect("truck-arrival-web")

@login_required
def record_departure_web(request, dispatch_id):
    dispatch = get_object_or_404(ShipmentDispatch, id=dispatch_id)

    dispatch.truck_depature = True
    dispatch.truck_depature_date = timezone.now()
    dispatch.save()

    shipment = dispatch.shipment
    shipment.departure_at_warehouse = True
    shipment.departure_at_warehouse_date = timezone.now()
    shipment.save(update_fields=[
        "departure_at_warehouse",
        "departure_at_warehouse_date"
    ])

    phase_master = ShipmentPhaseMaster.objects.get(id=11)
    ShipmentPhase.objects.create(
        shipment=shipment,
        phase_code=phase_master.phase_code,
        phase_name=phase_master.phase_name,
        completed=True,
        completed_at=timezone.now(),
        updated_by=request.user,
        order=phase_master.order,
    )

    messages.success(request, "Departure recorded successfully.")
    return redirect("truck-arrival-web")



####################  WS 
@login_required
def ws_dashboard(request):
    if not request.user.groups.filter(name="Warehouse Staff").exists():
        return render(request, "dashboard/access_denied.html")

    record_grn = Shipment.objects.filter(
        arrival_at_warehouse=True,
        grn_complete_at_warehouse=False,
        grn_upload_at_warehouse=False
    ).count()

    return render(
        request,
        "ws/dashboard_ws.html",
        {"record_grn": record_grn}

    )







#@login_required
#def grn_record_web(request):
    # Only Warehouse Staff
    #if not request.user.groups.filter(name="Warehouse Staff").exists():
       # return render(request, "dashboard/access_denied.html")

    #return render(request, "ws/grn_record.html")




@login_required
def grn_record_web(request):
    # Only Warehouse Staff
    if not request.user.groups.filter(name="Warehouse Staff").exists():
        return render(request, "dashboard/access_denied.html")

    shipments = Shipment.objects.filter(
        arrival_at_warehouse=True,
        grn_upload_at_warehouse=False
    ).select_related("dispatch")

    context = {
        "shipments": shipments
    }
    return render(request, "ws/grn_record.html", context)   


#!!!!!!! physical stck count
@login_required
def verify_physical_stock_web(request, shipment_id):
    if not request.user.groups.filter(name="Warehouse Staff").exists():
        return render(request, "dashboard/access_denied.html")

    shipment = get_object_or_404(
        Shipment,
        id=shipment_id,
        arrival_at_warehouse=True
    )

    if request.method == "POST":
        shipment.physical_stock_verified = True
        shipment.save()

        messages.success(
            request,
            f"Physical stock verified for {shipment.shipment_code}"
        )

    return redirect("grn-record-web")




@login_required
def record_grn_upload_web(request, shipment_id):
    if not request.user.groups.filter(name="Warehouse Staff").exists():
        return render(request, "dashboard/access_denied.html")

    ###shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment = get_object_or_404(
        Shipment,
        id=shipment_id,
        physical_stock_verified=True   # 🔐 ENFORCED
    )

    if request.method == "POST":
        grn_number = request.POST.get("grn_number", "").strip()
        receiving_notes = request.POST.get("receiving_notes", "")
        ##physical_stock_verified = request.POST.get("physical_stock_verified") == "on"
        #grn_uploaded = request.POST.get("grn_uploaded") == "on"

        if not grn_number:
            messages.error(request, "GRN Number is required.")
            return redirect("grn-record-web")

        shipment.grn_number = grn_number
        shipment.receiving_notes = receiving_notes
        ###shipment.physical_stock_verified = physical_stock_verified
        ###shipment.grn_upload_at_warehouse = True
        ###shipment.grn_uploaded = grn_uploaded

        ##if physical_stock_verified and grn_uploaded:
        shipment.grn_upload_at_warehouse = True
        shipment.grn_upload_at_warehouse_date = timezone.now()

        shipment.save()

        # Phase logging
        try:
            phase_master = ShipmentPhaseMaster.objects.get(id=12)
            ShipmentPhase.objects.create(
                shipment=shipment,
                phase_code=phase_master.phase_code,
                phase_name=phase_master.phase_name,
                completed=True,
                completed_at=timezone.now(),
                updated_by=request.user,
                order=phase_master.order,
            )
        except ShipmentPhaseMaster.DoesNotExist:
            pass

        messages.success(
            request,
            f"GRN recorded successfully for {shipment.shipment_code}"
        )

    return redirect("grn-record-web")




    #########################   Import Department
@login_required
def imports_dashboard(request):
    today = timezone.now().date()
    current_month_filter = Q(order_date__month=today.month, order_date__year=today.year)
    pending_grn_count = Shipment.objects.filter(
        grn_complete_at_warehouse=False,
        grn_upload_at_warehouse=True
    ).count()
    
    dispatch_count = Shipment.objects.filter(
        ship_dispatch=True     
    ).count()

    total_shipments = Shipment.objects.filter(
        current_month_filter, ship_status__gt=1
    ).count()

    completed_shipments = Shipment.objects.filter(ship_status=13).count()
    active_shipments = Shipment.objects.filter(ship_status__lt=13).count()

    on_the_way_shipment = Shipment.objects.filter(
        C_Process_completed=True,
        arrival_at_warehouse=False
    ).count()

    approved_duty_payments = Shipment.objects.filter(
        duty_paid=True
    ).count()
   
    
    return render(request, "dash/imp_dashboard.html", {
        "pending_grn_count": pending_grn_count,
        "total_shipments": total_shipments,
        "completed_shipments": completed_shipments,
        "active_shipments": active_shipments,
        "on_the_way_shipment": on_the_way_shipment,
        "approved_duty_payments": approved_duty_payments,
        "dispatch_count": dispatch_count,
    })


@login_required
def grn_confirm_web(request):
    shipments = Shipment.objects.filter(
        grn_complete_at_warehouse=False,
        grn_upload_at_warehouse=True
    ).select_related("dispatch", "supplier")

    return render(request, "imp/grn_confirm_web.html", {
        "shipments": shipments
    })


@login_required
def record_grn_confirm_web(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    shipment.grn_complete_at_warehouse = True
    shipment.grn_complete_at_warehouse_date = timezone.now()
    shipment.ship_status = 13
    shipment.save()

    # Phase history
    try:
        phase_master = ShipmentPhaseMaster.objects.get(id=13)
        ShipmentPhase.objects.create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            phase_name=phase_master.phase_name,
            completed=True,
            completed_at=timezone.now(),
            updated_by=request.user,
            order=phase_master.order,
        )
    except ShipmentPhaseMaster.DoesNotExist:
        pass

    messages.success(
        request,
        f"GRN confirmed successfully for shipment {shipment.shipment_code}"
    )

    return redirect("grn_confirm_list")




################### Dashboard KPI 

@login_required
def dashboard_kpi_web(request):
    user = request.user
    today = timezone.now().date()

    current_month_filter = Q(
        order_date__month=today.month,
        order_date__year=today.year
    )

    # ================= COMMON STATS =================
    total_shipments_month = Shipment.objects.filter(
        current_month_filter, ship_status__gt=1
    ).count()

    completed_shipments = Shipment.objects.filter(ship_status=13).count()
    active_shipments = Shipment.objects.filter(ship_status__lt=13).count()

    overdue_shipments = Shipment.objects.filter(
        expected_arrival_date__lt=today
    ).exclude(ship_status=13).count()

    on_the_way_shipment = Shipment.objects.filter(
        C_Process_completed=True,
        arrival_at_warehouse=False
    ).count()

    # ================= CLEARANCE =================
    clearance_initiated = Shipment.objects.filter(
        C_Process_Initiated=True,
        C_Process_completed=False
    ).count()

    clearance_completed = Shipment.objects.filter(
        C_Process_completed=True
    ).count()

    goods_at_port = Shipment.objects.filter(
        C_Process_Initiated=False
    ).count()

    # ================= BANK =================
    total_invoice_value = (
        Shipment.objects.aggregate(total=Sum("amount"))["total"] or 0
    )

    approved_duty_payments = Shipment.objects.filter(
        duty_paid=True
    ).count()

    pending_bank_docs = Shipment.objects.filter(ship_status=1).count()

    total_amount_pending = (
        BankDocument.objects.filter(settled=False)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    # ================= GRN =================
    pending_grn = Shipment.objects.filter(
        arrival_at_warehouse=True,
        grn_complete_at_warehouse=False
    ).count()

    record_grn = Shipment.objects.filter(
        arrival_at_warehouse=True,
        grn_complete_at_warehouse=False,
        grn_upload_at_warehouse=False
    ).count()

    confirm_grn = Shipment.objects.filter(
        grn_complete_at_warehouse=False,
        grn_upload_at_warehouse=True
    ).count()

    total_grn_value_month = (
        Shipment.objects.filter(
            grn_complete_at_warehouse_date__month=today.month
        ).aggregate(total=Sum("amount"))["total"] or 0
    )

    # ================= ROLE-BASED DATA =================
    context = {
        "common": {
            "total_shipments_month": total_shipments_month,
            "completed_shipments": completed_shipments,
            "active_shipments": active_shipments,
            "overdue_shipments": overdue_shipments,
            "on_the_way_shipment": on_the_way_shipment,
        }
    }

    if user.groups.filter(name="Imports Department").exists():
        context["import"] = {
            "goods_at_port": goods_at_port,
            "clearance_initiated": clearance_initiated,
            "clearance_completed": clearance_completed,
            "pending_grn": pending_grn,
            "confirm_grn": confirm_grn,
            "total_grn_value_month": total_grn_value_month,
            "total_invoice_value": total_invoice_value,
            "approved_duty_payments": approved_duty_payments,
            "pending_bank_docs": pending_bank_docs,
        }

    if user.groups.filter(name="Warehouse Staff").exists():
        context["ws"] = {
            "record_grn": record_grn,
        }

    if user.groups.filter(name="Bank Controller").exists():
        context["bank"] = {
            "pending_bank_docs": pending_bank_docs,
            "total_amount_pending": total_amount_pending,
            "approved_duty_payments": approved_duty_payments,
            "pending_grn": pending_grn,
        }

    if user.groups.filter(name="Managing Director").exists():
        context["md"] = {
            "total_invoice_value": total_invoice_value,
            "approved_duty_payments": approved_duty_payments,
            "clearance_initiated": clearance_initiated,
            "clearance_completed": clearance_completed,
            "pending_grn": pending_grn,
            "total_grn_value_month": total_grn_value_month,
        }

    return render(request, "dashboard_kpi_web.html", context)



    ############## shipments 
from django.db.models import Q, Exists, OuterRef
from .models import ShipmentPhase
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

@login_required

def shipments_web(request):
    status = request.GET.get("status", "Active")
    q = request.GET.get("q", "").strip()
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    page_number = request.GET.get("page", 1)

    statuses = ["Active", "Completed", "All"]

    base_qs = Shipment.objects.select_related("supplier").order_by("-id")

    # 🔍 Check if user applied any filter
    is_dashboard = not (start_date or end_date or q)

    # =====================
    # DASHBOARD MODE
    # =====================
    if is_dashboard:
        active_shipments = base_qs.exclude(ship_status=13)
        last_shipments = base_qs[:10]

        return render(
            request,
            "shipments/shipments_web.html",
            {
                "dashboard": True,
                "active_shipments": active_shipments,
                "last_shipments": last_shipments,
                "status": status,
                "statuses": statuses,
                "q": q,
            }
        )

    # =====================
    # FULL LIST MODE
    # =====================
    queryset = base_qs

    if status == "Completed":
        queryset = queryset.filter(ship_status=13)
    elif status == "Active":
        queryset = queryset.exclude(ship_status=13)

    if q:
        queryset = queryset.filter(
            Q(bl__icontains=q) |
            Q(supplier__supplier_name__icontains=q)
        )

    if start_date:
        queryset = queryset.filter(order_date__gte=start_date)

    if end_date:
        queryset = queryset.filter(order_date__lte=end_date)

    paginator = Paginator(queryset, 12)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "shipments/shipments_web.html",
        {
            "dashboard": False,
            "shipments": page_obj,
            "page_obj": page_obj,
            "status": status,
            "statuses": statuses,
            "q": q,
            "start_date": start_date,
            "end_date": end_date,
        }
    )




    #################### bank settlemenet ###############

@login_required
def bank_document_settlement_web(request):
    context = {
        "doc_types": ["ALL", "DA", "DP", "LC", "TT", "IMP"]
    }
    return render(
        request,
        "bc/bank_document_settlement_web.html",
        context
    )



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from .models import BankDocument, Settlement

@login_required
def add_settlement_web(request, doc_id):
    document = get_object_or_404(BankDocument, pk=doc_id)

    # ---------- Calculate outstanding balance ----------
    total_settled = (
        Settlement.objects
        .filter(document=document)
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    outstanding_amount = (document.amount or 0) - total_settled

    context = {
        "document": document,
        "outstanding_amount": outstanding_amount,
    }

    if request.method == "POST":
        settlement_type = request.POST.get("settlement_type")
        settlement_date = request.POST.get("settlement_date")
        amount = request.POST.get("amount")
        reference_number = request.POST.get("reference_number")
        remarks = request.POST.get("remarks")
        due_date = request.POST.get("due_date") or None

        # ---------- Validation ----------
        if not amount or float(amount) <= 0:
            context["error"] = "Settlement amount must be greater than 0"
            return render(request, "bc/add_settlement_web.html", context)

        if float(amount) > outstanding_amount:
            context["error"] = "Settlement amount cannot exceed outstanding balance"
            return render(request, "bc/add_settlement_web.html", context)

        if settlement_type == "IMP" and not due_date:
            context["error"] = "IMP Due Date is required"
            return render(request, "bc/add_settlement_web.html", context)

        # ---------- Create Settlement ----------
        Settlement.objects.create(
            document=document,
            settlement_type=settlement_type,
            settlement_date=settlement_date,
            amount=amount,
            reference_number=reference_number,
            remarks=remarks,
            created_by=request.user,
        )

        # ---------- Create IMP BankDocument ----------
        if settlement_type == "IMP":
            BankDocument.objects.create(
                shipment=document.shipment,
                bank=document.bank,
                doc_type="IMP",
                reference_number=reference_number,
                company=document.company,
                amount=amount,
                issue_date=timezone.now().date(),
                due_date=due_date,
                settlement_date=settlement_date,
                created_by=request.user,
            )

        return redirect("bank_document_settlement_web")

    return render(request, "bc/add_settlement_web.html", context)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def bank_document_report_web(request):
    return render(
        request,
        "bc/bank_document_report_web.html"
    )




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.dateparse import parse_date
from .models import BankDocument, Settlement, Company

@login_required
def outstanding_report_web(request):
    companies = Company.objects.all().order_by("name")
    doc_types = ["ALL", "DA", "DP", "TT", "IMP"]

    results = []
    selected_company = ""
    selected_doc_type = "ALL"
    as_at = ""

    if request.method == "POST":
        selected_company = request.POST.get("company_id") or ""
        selected_doc_type = request.POST.get("doc_type") or "ALL"
        as_at = request.POST.get("date")

        as_at_date = parse_date(as_at)

        documents = BankDocument.objects.select_related("company")

        if selected_company:
            documents = documents.filter(company_id=selected_company)

        if selected_doc_type != "ALL":
            documents = documents.filter(doc_type=selected_doc_type)

        for doc in documents:
            settled_amount = (
                Settlement.objects
                .filter(
                    document=doc,
                    settlement_date__lte=as_at_date
                )
                .aggregate(total=Sum("amount"))["total"] or 0
            )

            balance = (doc.amount or 0) - settled_amount

            if balance > 0:
                results.append({
                    "company": doc.company.name if doc.company else "",
                    "doc_type": doc.doc_type,
                    "reference_number": doc.reference_number,
                    "amount": doc.amount or 0,
                    "balance": balance,
                })

    context = {
        "companies": companies,
        "doc_types": doc_types,
        "results": results,
        "selected_company": selected_company,
        "selected_doc_type": selected_doc_type,
        "as_at": as_at,
        "total_amount": sum([item["amount"] for item in results]),
        "total_balance": sum([item["balance"] for item in results]),
    }

    return render(
        request,
        "bc/outstanding_report_web.html",
        context
    )

from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce

def get_outstanding_results(request):
    company_id = request.POST.get("company_id") or request.GET.get("company_id")
    doc_type = request.POST.get("doc_type") or request.GET.get("doc_type")
    as_at = request.POST.get("date") or request.GET.get("date")

    qs = BankDocument.objects.annotate(
        settled_amount=Coalesce(
            Sum("settlements__amount"),
            0,
            output_field=DecimalField(max_digits=18, decimal_places=2)
        ),
        outstanding=F("amount") - Coalesce(
            Sum("settlements__amount"),
            0,
            output_field=DecimalField(max_digits=18, decimal_places=2)
        )
    )

    if as_at:
        qs = qs.filter(issue_date__lte=as_at)

    if company_id:
        qs = qs.filter(company_id=company_id)

    if doc_type and doc_type != "ALL":
        qs = qs.filter(doc_type=doc_type)

    qs = qs.filter(outstanding__gt=0)

    return qs


#from django.http import HttpResponse
#from reportlab.pdfgen import canvas
#from django.template.loader import get_template
#from xhtml2pdf import pisa

#@login_required


#def outstanding_report_pdf(request):
   # results = get_outstanding_results(request)

   # template = get_template("reports/outstanding_pdf.html")
   # html = template.render({"results": results})

#response = HttpResponse(content_type="application/pdf")
#response["Content-Disposition"] = 'attachment; filename="outstanding_report.pdf"'

   # pisa.CreatePDF(html, dest=response)
   # return response




####################### Bank dahboard
from django.shortcuts import render
from django.db.models import Sum
from .models import Bank, BankDocument

def bank_dashboard_web(request):
    banks = Bank.objects.all()
    dashboard_data = []

    for bank in banks:
        # IMP calculations
        imp_used = (
            BankDocument.objects
            .filter(bank=bank, doc_type="IMP")
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        imp_limit = bank.imp or 0
        imp_balance = imp_limit - imp_used
        imp_utilization = (imp_used / imp_limit * 100) if imp_limit > 0 else 0

        # DA calculations
        da_used = (
            BankDocument.objects
            .filter(bank=bank, doc_type="DA")
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        da_limit = bank.da or 0
        da_balance = da_limit - da_used

        dashboard_data.append({
            "bank": bank,
            "imp_limit": imp_limit,
            "imp_used": imp_used,
            "imp_balance": imp_balance,
            "imp_utilization": round(imp_utilization, 1),

            "da_limit": da_limit,
            "da_used": da_used,
            "da_balance": da_balance,
        })

    context = {
        "dashboard_data": dashboard_data
    }
    return render(request, "bank/bank_dashboard.html", context)



from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone   # ✅ THIS WAS MISSING
from .models import Bank, BankDocument

def bank_dashboard_data(request):
    data = []

    for bank in Bank.objects.all():
        imp_used = BankDocument.objects.filter(
            bank=bank, doc_type="IMP"
        ).aggregate(total=Sum("amount"))["total"] or 0

        imp_limit = bank.imp or 0
        imp_balance = imp_limit - imp_used
        utilization = (imp_used / imp_limit * 100) if imp_limit else 0

        da_used = BankDocument.objects.filter(
            bank=bank, doc_type="DA"
        ).aggregate(total=Sum("amount"))["total"] or 0

        da_limit = bank.da or 0
        da_balance = da_limit - da_used

        data.append({
            "bank_id": bank.b_id,
            "imp_limit": float(imp_limit),
            "imp_used": float(imp_used),
            "imp_balance": float(imp_balance),
            "utilization": round(utilization, 1),
            "da_limit": float(da_limit),
            "da_used": float(da_used),
            "da_balance": float(da_balance),
        })

    return JsonResponse({
        "timestamp": timezone.now().strftime("%I:%M %p"),
        "banks": data
    })



from django.utils.timezone import now

def ca_history(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    search = request.GET.get('search')

    qs = Shipment.objects.filter(
        clearing_agent=request.user
    ).order_by('-updated_at')

    if from_date and to_date:
        qs = qs.filter(updated_at__date__range=[from_date, to_date])

    if search:
        qs = qs.filter(reference_no__icontains=search)

    context = {
        'shipments': qs,
        'from_date': from_date,
        'to_date': to_date,
        'search': search,
    }
    return render(request, 'clearing_agent/history.html', context)



#############md special dashboard
# masters/views.py (or dashboard/views.py)

from django.contrib.auth.decorators import login_required
#from .services import get_bank_dashboard_data
from .services import get_sales_dashboard_data


from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

# import sales service


# import bank models
from .models import Bank, BankDocument

@login_required
def md_dashboard_web(request):

    # ================= BANK DATA (same as bank_dashboard_web) =================
    banks = Bank.objects.all()
    dashboard_data = []

    for bank in banks:
        imp_used = BankDocument.objects.filter(
            bank=bank, doc_type="IMP"
        ).aggregate(total=Sum("amount"))["total"] or 0

        imp_limit = bank.imp or 0
        imp_balance = imp_limit - imp_used
        imp_utilization = (imp_used / imp_limit * 100) if imp_limit else 0

        da_used = BankDocument.objects.filter(
            bank=bank, doc_type="DA"
        ).aggregate(total=Sum("amount"))["total"] or 0

        da_limit = bank.da or 0
        da_balance = da_limit - da_used
        da_utilization = (da_used / da_limit * 100) if da_limit else 0

        dashboard_data.append({
            "bank": bank,
            "imp_limit": imp_limit,
            "imp_used": imp_used,
            "imp_balance": imp_balance,
            "imp_utilization": round(imp_utilization, 1),
            "da_limit": da_limit,
            "da_used": da_used,
            "da_balance": da_balance,
            "da_utilization": round(da_utilization, 1),
        })

    bank_context = {
        "dashboard_data": dashboard_data,
        "today": timezone.now().date(),
    }

    # ================= SALES DATA (reuse existing service) =================
    sales_context = get_sales_dashboard_data()

    # ================= MERGE =================
    context = {
        **bank_context,
        **sales_context,
    }

    return render(request, "md/md_dashboard_new.html", context)




############# asynchrinize web page
from django.http import JsonResponse
from django.db.models import OuterRef, Subquery, IntegerField, Value, Case, When, F, Sum
from django.utils import timezone
from django.db.models import DateField

TOTAL_PHASES = 7  # adjust if needed

@login_required
def md_dashboard_data_api(request):

    # ================= PHASE SUBQUERIES =================
    latest_phase_order = ShipmentPhase.objects.filter(
        shipment=OuterRef("pk")
    ).order_by("-order").values("order")[:1]

    latest_phase_name = ShipmentPhase.objects.filter(
        shipment=OuterRef("pk")
    ).order_by("-order").values("phase_name")[:1]

    # ================= SHIPMENTS =================
    shipments_qs = (
        Shipment.objects
        .filter(grn_complete_at_warehouse=False)
        .select_related("supplier")
        .annotate(
            phase_order=Subquery(latest_phase_order, output_field=IntegerField()),
            current_phase=Subquery(latest_phase_name),
            arrival_date=Coalesce(
            "ship_arival_date",
            "expected_arrival_date",
            output_field=DateField()
        )
        )
        .annotate(
            progress=Case(
                When(phase_order__isnull=True, then=Value(0)),
                default=(F("phase_order") * 100 / TOTAL_PHASES),
                output_field=IntegerField(),
            )
        )
        .order_by("arrival_date")
    )

    shipments = []
    for s in shipments_qs:
        shipments.append({
            "shipment_code": s.shipment_code,
            "supplier": s.supplier.supplier_name if s.supplier else "-",
           "arrival": (
    s.arrival_date.strftime("%b %d, %Y")
    if s.arrival_date
    else "-"
),

            "phase": s.current_phase or "-",
            "progress": min(s.progress, 100),
        })

    # ================= KPIs =================
    kpis = {
        "total_active": Shipment.objects.filter(grn_complete_at_warehouse=False).count(),
        "new": Shipment.objects.filter(ship_status=1).count(),
        "at_port": Shipment.objects.filter(
            C_Process_Initiated=True,
            C_Process_completed=False
        ).count(),
        "on_the_way": Shipment.objects.filter(
            C_Process_completed=True,
            arrival_at_warehouse=False
        ).count(),
        "grn": Shipment.objects.filter(
            grn_upload_at_warehouse=True,
            grn_complete_at_warehouse=False
        ).count(),
        "completed": Shipment.objects.filter(grn_complete_at_warehouse=True).count(),
    }

    # ================= BANKS =================
    banks_data = []

    for bank in Bank.objects.all():
        imp_used = BankDocument.objects.filter(
            bank=bank, doc_type="IMP"
        ).aggregate(total=Sum("amount"))["total"] or 0

        da_used = BankDocument.objects.filter(
            bank=bank, doc_type="DA"
        ).aggregate(total=Sum("amount"))["total"] or 0

        imp_limit = bank.imp or 0
        da_limit = bank.da or 0

        banks_data.append({
            "bank": bank.b_name,
            "accno": bank.accno,
            "imp_balance": imp_limit - imp_used,
            "imp_limit": imp_limit,
            "imp_utilization": round(((imp_limit -imp_used) / imp_limit * 100), 1) if imp_limit else 0,
            "da_balance": da_limit - da_used,
            "da_limit": da_limit,
            "da_utilization": round(((da_limit-da_used) / da_limit * 100), 1) if da_limit else 0,
        })

    # ================= RESPONSE =================
    return JsonResponse({
        "kpis": kpis,
        "shipments": shipments,
        "banks": banks_data,
    })
