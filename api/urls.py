from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('organizer/', views.organizer_views),
    path('organizer/<int:organizer_id>/', views.get_organizer_by_id),
    path('events/<int:event_id>/', views.list_events_by_id),
    path('events/', views.event_views),
    path('events/<int:event_id>/ticket-types/', views.ticket_type_views),
    path('orders/', views.create_order),
    path('payments/nomba/webhook/', views.NombaWebhookView),
]


