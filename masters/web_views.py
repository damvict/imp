from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ArrivalNoticeForm
from .services import create_arrival_notice


@login_required
def create_arrival_notice_view(request):

    if request.method == "POST":
        form = ArrivalNoticeForm(request.POST)

        if form.is_valid():
            shipment = create_arrival_notice(
                form.cleaned_data,
                request.user
            )

            # ✅ Render same page with success modal data
            return render(
                request,
                "masters/arrival_notice_form.html",
                {
                    "form": ArrivalNoticeForm(),   # fresh empty form
                    "success": True,
                    "shipment_code": shipment.shipment_code,
                }
            )

    else:
        form = ArrivalNoticeForm()

    return render(
        request,
        "masters/arrival_notice_form.html",
        {"form": form},
    )


##~~~~~~~~~~~~~~ End


############ Shipment TimeLine View ###################

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Shipment, ShipmentPhase


@login_required
def shipment_timeline(request, shipment_code):
    shipment = get_object_or_404(
        Shipment,
        shipment_code=shipment_code
    )

    phases = ShipmentPhase.objects.filter(
        shipment=shipment
    ).order_by("order")

    # detect if user came right after creation
    from_create = request.GET.get("from") == "create"

    return render(
        request,
        "shipments/shipment_timeline.html",
        {
            "shipment": shipment,
            "phases": phases,
            "from_create": from_create,
        }
    )



############## New Shipment View ####################

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Shipment
from .forms import NewShipmentForm
from .services import update_shipment_stage


@login_required
def new_shipment_view(request):

    # 🔹 Arrival notices only (ship_status = 1)
    arrival_shipments = Shipment.objects.filter(
        ship_status=1
    ).order_by("-created_at")

    if request.method == "POST":
        form = NewShipmentForm(request.POST)

        if form.is_valid():
            #shipment_id = form.cleaned_data["shipment"]
            shipment = form.cleaned_data["shipment"]

            update_shipment_stage(
                {
                    **form.cleaned_data,
                    "shipment_id": shipment.id,
                    "company": shipment.company_id,
                },
                request.user
            )

            return redirect(
                "shipment-timeline",
                shipment_code=shipment.shipment_code
            )

    else:
        form = NewShipmentForm()

    return render(
        request,
        "shipments/new_shipment.html",
        {
            "form": form,
            "arrival_shipments": arrival_shipments,
        }
    )
##~~~~~~~~~~~~~~ End


