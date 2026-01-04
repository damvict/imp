from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import (
    WarehouseListView, WarehouseCreateView, WarehouseUpdateView, WarehouseDeleteView,
    CompanyListView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView,
    SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView,
    ClearingAgentListView, ClearingAgentCreateView, ClearingAgentUpdateView, ClearingAgentDeleteView,
    BankListView, BankCreateView, BankUpdateView, BankDeleteView,
    ShipmentDispatchCreateView,
)

from .views import (
    bank_dashboard,
    bank_doc_types,
    incoterms,
    transport_modes,
    shipment_types,
    confirm_handover,
    shipment_detail_api,
    get_next_shipment_code,
    bank_documents_summary,
    clearing_agent_users,
    outstanding_report,
    outstanding_export_excel,
    outstanding_report_email,
)

urlpatterns = [

    # ---------------- MASTER DATA ----------------
    path('itemcategory/', views.itemcategory_list),
    path('itemcategory/create/', views.itemcategory_create),
    path('itemcategory/edit/<int:pk>/', views.itemcategory_edit),
    path('itemcategory/delete/<int:pk>/', views.itemcategory_delete),

    path('vehicletypes/', views.vehicle_type_list),
    path('vehicletypes/create/', views.vehicle_type_create),
    path('vehicletypes/edit/<int:pk>/', views.vehicle_type_edit),
    path('vehicletypes/delete/<int:pk>/', views.vehicle_type_delete),

    path('statuscolors/', views.status_color_list),
    path('statuscolors/create/', views.status_color_create),
    path('statuscolors/edit/<int:pk>/', views.status_color_edit),
    path('statuscolors/delete/<int:pk>/', views.status_color_delete),

    path('salesdivisions/', views.salesdivision_list),
    path('salesdivisions/create/', views.salesdivision_create),
    path('salesdivisions/edit/<int:pk>/', views.salesdivision_edit),
    path('salesdivisions/delete/<int:pk>/', views.salesdivision_delete),

    # ---------------- COMPANIES ----------------
    path('companies/', CompanyListView.as_view()),
    path('companies/create/', CompanyCreateView.as_view()),
    path('companies/<int:pk>/edit/', CompanyUpdateView.as_view()),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view()),

    # ---------------- SUPPLIERS ----------------
    path('suppliers/', SupplierListView.as_view()),
    path('suppliers/create/', SupplierCreateView.as_view()),
    path('suppliers/<int:pk>/update/', SupplierUpdateView.as_view()),
    path('suppliers/<int:pk>/delete/', SupplierDeleteView.as_view()),

    # ---------------- CLEARING AGENTS ----------------
    path('clearingagents/', ClearingAgentListView.as_view()),
    path('clearingagents/add/', ClearingAgentCreateView.as_view()),
    path('clearingagents/<int:pk>/edit/', ClearingAgentUpdateView.as_view()),
    path('clearingagents/<int:pk>/delete/', ClearingAgentDeleteView.as_view()),

    # ---------------- SHIPMENTS ----------------
    path('shipments/', views.shipment_list),
    path('shipments/create/', views.shipment_create),
    path('shipment/edit/<int:pk>/', views.shipment_edit),
    path('shipment/delete/<int:pk>/', views.shipment_delete),

    # ---------------- BANK CONTROLLER ----------------
    path('bank-controller/', views.bank_controller_view),
    path('bank-controller/update/<int:shipment_id>/bank-update/', views.bank_controller_update),

    # ---------------- BANK MANAGER ----------------
    path('bank-manager/', views.bank_manager_view),
    path('bank-manager/update/<int:shipment_id>/bank-update/', views.bank_manager_update),

    # ---------------- ARRIVAL / UNLOADING ----------------
    path('shipments/pending-arrival/', views.pending_arrival_list),
    path('shipments/details/<int:detail_id>/arrival-update/', views.arrival_update_detail),

    path('shipments/pending-unloading/', views.pending_unloading_list),
    path('shipments/start-unloading/<int:pk>/', views.start_unloading),
    path('shipments/complete-unloading/', views.unloading_in_progress_list),
    path('shipments/finish_unloading/<int:pk>/', views.finish_unloading),

    # ---------------- CLEARING AGENT ----------------
    path('clearing-agent/shipments/', views.clearing_agent_shipments_view),
    path('clearing-agent/upload/<int:shipment_id>/', views.upload_assessment_document_view),

    # ---------------- WAREHOUSE ----------------
    path('warehouses/', WarehouseListView.as_view()),
    path('warehouses/create/', WarehouseCreateView.as_view()),
    path('warehouses/update/<int:pk>/', WarehouseUpdateView.as_view()),
    path('warehouses/delete/<int:pk>/', WarehouseDeleteView.as_view()),

    # ---------------- DASHBOARDS ----------------
    path('shipments/admin-dashboard/', views.admin_dashboard),
    path('shipments/warehouse-dashboard/', views.warehouse_dashboard),
    path('shipments/md-dashboard/', views.md_dashboard),

    # ---------------- API ----------------
    path('api/upload-assessment/<int:shipment_id>/', views.upload_assessment_document),
    path('api/dispatch/<int:shipment_id>/', ShipmentDispatchCreateView.as_view()),

    path('api/bank-dashboard/', bank_dashboard),
    path('api/shipments/next-code/', get_next_shipment_code),

    path('api/bank-doc-types/', bank_doc_types),
    path('api/incoterms/', incoterms),
    path('api/transport-modes/', transport_modes),
    path('api/shipment-types/', shipment_types),

    path('api/bank-documents/', views.bank_documents_list),
    path('api/bank-summary/', bank_documents_summary),

    path('api/confirm-handover/<int:shipment_id>/', confirm_handover),

    path('api/shipment-phase/<int:shipment_id>/', shipment_detail_api),

    path("api/reports/outstanding/", outstanding_report),
    path("api/outstanding/export/", outstanding_export_excel),
    path("api/outstanding/email/", outstanding_report_email),
]

# ---------------- MEDIA FILES (CRITICAL FIX) ----------------
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
