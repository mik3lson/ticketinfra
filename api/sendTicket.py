#send Ticket to user email

from django.core.mail import send_mail
from django.conf import settings    

"""
def send_ticket_email(ticket, user_email):
    subject = f"Your Ticket for {ticket.ticket_type.event.name}"
    message = f"Hello,\n\nHere is your ticket for the event '{ticket.ticket_type.event.name}':\n\nTicket ID: {ticket.ticket_id}\nTicket Type: {ticket.ticket_type.name}\nEvent Date: {ticket.ticket_type.event.date}\n\nThank you for your purchase!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

"""