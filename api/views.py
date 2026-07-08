from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Organizer, Apikey, Event, TicketType, Order, Ticket
from .serializers import OrganizerSerializer, ApikeySerializer, EventSerializer, TicketTypeSerializer, OrderSerializer, TicketSerializer
from django.db import transaction
from django.utils import timezone
from django.db import models
from django.shortcuts import get_object_or_404




@api_view(['GET'])
def home(response):
    return Response({"TicketInfra API"})


#get all Organizer
def get_organizer(request):
    organizer = Organizer.objects.all()
    serializer = OrganizerSerializer(organizer, many=True)
    return Response(serializer.data)


#get organizer by id
@api_view(['GET'])
def get_organizer_by_id(request, organizer_id):
    try:
        organizer = Organizer.objects.get(id=organizer.id)
    except Organizer.DoesNotExist:
        return Response({"error": "Organiser not found"}, status=404)
    
    serializer = OrganizerSerializer(organizer)
    return Response(serializer.data)

#create a new organizer
def create_organizer(request):
    serializer = OrganizerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['GET', 'POST'])
def organizer_views(request):
    if request.method == 'POST':
        return create_organizer(request)
    elif request.method == 'GET':
        return get_organizer(request)







#create an event
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


#list all events for a organizer
@api_view(['GET'])
def list_events_by_id(request, organizer_id):
    events = Event.objects.filter(organizer_id=organizer_id)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=200)

#list all events 
def list_all_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET', 'POST'])
def event_views(request):
    if request.method == 'POST':
        return create_event(request)
    elif request.method == 'GET':
        return list_all_events(request)






#create a ticket type for an event

def add_ticket_type(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    serializer = TicketTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(event=event)
        return Response(serializer.data, status= 201)

    return Response(serializer.errors, status=400)


#list all ticket types for an event
def list_ticket_types(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    ticket_types = TicketType.objects.filter(event=event)
    serializer = TicketTypeSerializer(ticket_types, many=True)
    return Response(serializer.data)



@api_view(['GET','POST'])
def ticket_type_views(request, event_id):
    if request.method == 'POST':
        return add_ticket_type(request, event_id)
    elif request.method == 'GET':
        return list_ticket_types(request, event_id)
























#create an order
@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            order = serializer.save()
            ticket_type = order.ticket_type
            if ticket_type.quantity < order.quantity:
                return Response({"error": "Not enough tickets available"}, status=400)
            ticket_type.quantity -= order.quantity
            ticket_type.save()

            #hold tickets for 10 minutes until payment is completed
            #  check if payment is completed
            # send email to user with ticket details
            order.created_at = timezone.now()
            for _ in range(order.quantity):
                Ticket.objects.create(order=order, ticket_type=ticket_type)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(['POST'])
def NombaWebhookView(request):
    # Handle the webhook payload
    payload = request.data
    # Process the payload as needed
    # For example, you can log it or update your database
    print("Received Nomba webhook:", payload)
    
    # Return a response to acknowledge receipt of the webhook
    return Response({"message": "Webhook received successfully."}, status=200)