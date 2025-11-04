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

from django.utils import timezone
#from .forms import ShipmentArrivalForm
from .models import ShipmentStatusHistory

from django.db.models import F, ExpressionWrapper, DurationField, Avg

from datetime import timedelta
from .models import Shipment, ShipmentDetail
from django.core.mail import send_mail

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
from django.utils import timezone
from .models import Shipment, ShipmentPhase, ShipmentPhaseMaster, StatusColor
from datetime import datetime


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
from django.utils import timezone
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
        payment_marked=False
    )

    return render(request, 'masters/bm_shipments.html', {'shipments': shipments})

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
from django.utils import timezone
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
from django.shortcuts import render, redirect
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
from django.utils import timezone
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
from django.utils import timezone
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
from django.shortcuts import render
from django.utils import timezone
from masters.models import StatusColor, ShipmentDetail, UserProfile

@login_required
def warehouse_dashboard(request):
    today = timezone.now().date()

    # Get the user's assigned warehouse
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_warehouse = user_profile.warehouse
    except UserProfile.DoesNotExist:
        user_warehouse = None

    if not user_warehouse:
        return render(request, 'dash/warehouse_dashboard.html', {
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

from django.shortcuts import render
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
from django.shortcuts import render

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

@login_required
@user_passes_test(is_md)
def md_dashboard(request):   
    # Filter shipments where payment is marked but duty not approved yet
    shipments = Shipment.objects.filter(payment_marked=True, duty_paid=False)

    context = {
        "shipments": shipments
    }
    return render(request, "dash/md_dashboard.html", context)

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
        send_to_clearing_agent_payment=True
    ).filter(
        ~Q(C_Process_Initiated=True)  # C_Process_Initiated != True
    )

    serializer = ClearingAgentShipmentSerializer(shipments, many=True)
    return Response(serializer.data)



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
        {"message": "Clearing Process Initiated successfully", "shipment": serializer.data},
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
from django.utils import timezone
from .models import Shipment

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_assessment_document(request, shipment_id):
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
    
    total_duty = request.data.get("total_duty_value")
    file = request.FILES.get("assessment_document")

    # ✅ Case 1: no file, only duty value update
    if not file and total_duty:
        shipment.total_duty_value = total_duty
        shipment.assessment_uploaded_date =  timezone.now()
        shipment.save()
        return Response({"message": "Duty value updated successfully"}, status=status.HTTP_200_OK)
    # ✅ Automatically create shipment phase record (handover phase)
    try:
        phase_master = ShipmentPhaseMaster.objects.get(id=4)  # adjust this ID to your actual handover phase
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
        return Response({"error": "Phase master not found"}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Case 2: file uploaded + duty value
    if file:
        shipment.assessment_document = file
        if total_duty:
            shipment.total_duty_value = total_duty
        shipment.assessment_uploaded_date = timezone.now().date()
        shipment.save()
        return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)

    return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)




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
from django.utils import timezone
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
        shipment.save()

        # ShipmentPhase creation
        phase_master = ShipmentPhaseMaster.objects.get(id=6)
        ShipmentPhase.objects.create(
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








###################################################################################3

from django.utils import timezone
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
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shipment_create_api(request):
    data = request.data
    try:
        stage = data.get('stage', 'arrival')  # 'arrival' or 'shipment'
        shipment_code = data.get('shipment_code') or None
        # === STEP 1: CREATE NEW ARRIVAL NOTICE ===
        if stage == 'arrival':
            shipment = Shipment.objects.create(
                bl=data.get('bl', '0'),
                vessel=data.get('vessel', ' '),
                order_date=parse_date(data.get('order_date')),
                expected_arrival_date=parse_date(data.get('expected_arrival_date')),
                cbm=data.get('cbm'),
                remark=data.get('remark', ''),
                company_id=data.get('company'),
                supplier_id=data.get('supplier'),
                created_by=request.user,
                ship_status=1,
                container=data.get('container', ' ')              

            )

            # Create ShipmentPhase for Arrival Notice
            phase_master = ShipmentPhaseMaster.objects.get(id=1)  # Phase 1
            ShipmentPhase.objects.create(
                shipment=shipment,
                phase_code=phase_master.phase_code,
                phase_name=phase_master.phase_name,
                completed=True,
                completed_at=timezone.now(),
                updated_by=request.user,
                order=phase_master.order
            )

            return Response({
                'success': True,
                'message': 'Arrival Notice created successfully',
                'shipment_id': shipment.id,
                'shipment_code': shipment.shipment_code, 
                'phase': phase_master.phase_name
            }, status=201)

        # === STEP 2: UPDATE SHIPMENT DETAILS (Doc Collected & Shipments Created) ===
        elif stage == 'shipment':
            shipment_id = data.get('shipment_id')
            if not shipment_id:
                return Response({'error': 'shipment_id is required for shipment stage'}, status=400)

            shipment = Shipment.objects.get(id=shipment_id)

            # Update shipment fields
            shipment.bank_doc_type = data.get('bank_doc_type')
            shipment.reference_number = data.get('reference_number')
            shipment.bank_id = data.get('bank')
            shipment.amount = data.get('amount')
            shipment.c_date = parse_date(data.get('c_date')) if data.get('c_date') else None
            shipment.shipment_type = data.get('shipment_type')
            shipment.incoterm = data.get('incoterm')
            shipment.transport_mode = data.get('transport_mode')
            shipment.origin_country = data.get('origin_country')
            shipment.destination_port = data.get('destination_port')
            shipment.clearing_agent_id = data.get('clearing_agent') or None
            shipment.ship_status = 2
            shipment.packing_list_ref = data.get('packing_list_ref')
            shipment.supplier_invoice = data.get('supplier_invoice')
            shipment.save()

            # ===== SHIPMENT PHASE =====
            phase_master = ShipmentPhaseMaster.objects.get(id=2)  # Phase 2
            shipment_phase, created = ShipmentPhase.objects.update_or_create(
                shipment=shipment,
                phase_code=phase_master.phase_code,
                defaults={
                    'phase_name': phase_master.phase_name,
                    'completed': True,
                    'completed_at': timezone.now(),
                    'updated_by': request.user,
                    'order': phase_master.order,
                }
            )

            # ===== BANK DOCUMENT =====
            bank_doc, created = BankDocument.objects.update_or_create(
                shipment=shipment,
                doc_type=data.get('bank_doc_type'),
                defaults={
                    'bank_id': data.get('bank'),
                    'reference_number': data.get('reference_number'),
                    'amount': data.get('amount'),
                    'issue_date': parse_date(data.get('c_date')) if data.get('c_date') else timezone.now().date(),
                    'created_by': request.user,
                    'due_date': parse_date(data.get('due_date')) if data.get('due_date') else timezone.now().date(),
                }
            )

            return Response({
                'success': True,
                'message': 'Shipment stage updated successfully',
                'shipment_id': shipment.id,
                'phase': phase_master.phase_name
            }, status=201)

        else:
            return Response({'error': 'Invalid stage value'}, status=400)

    except Shipment.DoesNotExist:
        return Response({'error': 'Shipment not found'}, status=404)
    except ShipmentPhaseMaster.DoesNotExist:
        return Response({'error': 'Shipment phase master not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
###############################    PHASE DISPLAY   ################################

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Shipment, ShipmentPhase

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shipment_detail_api(request, shipment_id):
    try:
        shipment = Shipment.objects.get(id=shipment_id)

        # Get all phases for this shipment
        phases = ShipmentPhase.objects.filter(shipment=shipment).order_by('order')
        phases_data = [
            {
                "id": phase.id,
                "title": phase.phase_name,
                "completed": phase.completed,
                "completed_at": phase.completed_at.strftime("%Y-%m-%d %H:%M:%S") if phase.completed_at else None
            }
            for phase in phases
        ]

        shipment_data = {
            "bl": shipment.bl,
            "vessel": shipment.vessel,
            "amount": shipment.amount,
            "expected_arrival_date": shipment.expected_arrival_date.strftime("%Y-%m-%d") if shipment.expected_arrival_date else None,
             "supplier": shipment.supplier.supplier_name 
        }

        return Response({
            "shipment": shipment_data,
            "phases": phases_data
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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Shipment
from .forms import BankControllerForm

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_handover(request, shipment_id):
    """
    Confirm shipment handover: sets send_to_clearing_agent=True, send_date=now,
    and creates a ShipmentPhase record for 'Arrival Notice' or the handover phase.
    """
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update shipment
    data = {
        "send_to_clearing_agent": True,
        "send_date": timezone.now()
    }
    form = BankControllerForm(data, instance=shipment)
    if form.is_valid():
        form.save()

        # ✅ Add a ShipmentPhase for Handover / Arrival Notice
        try:
            phase_master = ShipmentPhaseMaster.objects.get(id=3)  # Adjust ID to your handover phase
            ShipmentPhase.objects.create(
                shipment=shipment,
                phase_code=phase_master.phase_code,
                phase_name=phase_master.phase_name,
                completed=True,
                completed_at=timezone.now(),
                updated_by=request.user,
                order=phase_master.order
            )
        except ShipmentPhaseMaster.DoesNotExist:
            return Response({"error": "Phase master not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Handover confirmed and phase recorded"})
    else:
        return Response({"error": form.errors}, status=status.HTTP_400_BAD_REQUEST)





##################### Bank Manager API
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Shipment
from .serializers import ShipmentSerializer

# GET all shipments for bank manager
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bank_manager_shipments_initiate(request):
    shipments = Shipment.objects.filter(
        send_to_clearing_agent=True,
        payment_marked=False
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
        C_Process_completed=False
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

    )
    serializer = ShipmentSerializer(shipments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_grn_upload(request, shipment_id):
  
    try:
        shipment = Shipment.objects.get(id=shipment_id)
    except Shipment.DoesNotExist:
        return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)

       
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
    total_shipments_month = Shipment.objects.filter(current_month_filter).count()
    completed_shipments = Shipment.objects.filter(ship_status=13).count()
    active_shipments = Shipment.objects.filter(ship_status__lt=13).count()
    overdue_shipments = Shipment.objects.filter(
        expected_arrival_date__lt=today,
    ).exclude(ship_status=13).count()
    on_the_way_shipments = Shipment.objects.filter(C_Process_Initiated=False).count()

    # Clearance stats
    clearance_initiated = Shipment.objects.filter(
        C_Process_Initiated=True, C_Process_completed=False
    ).count()
    clearance_completed = Shipment.objects.filter(C_Process_completed=True).count()
    goods_at_port = Shipment.objects.filter(C_Process_Initiated=False).count()

    # Bank data
    pending_bank_docs = Shipment.objects.filter(ship_status=1).count()
    total_amount_pending = (
        BankDocument.objects.filter(settled=False).aggregate(total=Sum('amount'))['total'] or 0
    )
    approved_duty_payments = Shipment.objects.filter(duty_paid=True).count()

    # GRN data
    pending_grn = Shipment.objects.filter(arrival_at_warehouse=True, grn_complete_at_warehouse=False).count()
    total_grn_value_month = (
        Shipment.objects.filter(grn_complete_at_warehouse_date__month=today.month)
        .aggregate(total=Sum('value'))['total'] or 0
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
            "on_the_way_shipments": on_the_way_shipments,
        }
    }

    if user.groups.filter(name="Bank Controller").exists():
        data["bank"] = {
            "pending_bank_docs": pending_bank_docs,
            "total_amount_pending": f"{total_amount_pending:,.2f}",
            "approved_duty_payments": approved_duty_payments,
        }

    if user.groups.filter(name="Import Department").exists():
        data["import"] = {
            "goods_at_port": goods_at_port,
            "clearance_initiated": clearance_initiated,
            "clearance_completed": clearance_completed,
            "pending_grn": pending_grn,
            "total_grn_value_month": f"{total_grn_value_month:,.2f}",
        }

    if user.groups.filter(name="Bank Manager").exists():
        data["bm"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
        }

    if user.groups.filter(name="Clearing Agent").exists():
        data["ca"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
        }

    if user.groups.filter(name="Managing Director").exists():
        data["md"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
        }   

    if user.groups.filter(name="Security Guard").exists():
        data["sg"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
        }

    if user.groups.filter(name="Warehouse Staff").exists():
        data["ws"] = {
            "total_invoice_value": f"{total_invoice_value:,.2f}",
            "approved_duty_payments": approved_duty_payments,
        }


    return Response(data)