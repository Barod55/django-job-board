from django.shortcuts import render
from .models import Info
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def send_message(request):
    myinfo = Info.objects.first()
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        # Here you would typically handle the message, e.g., save it or send an email
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # From settings
            [email],  # Send to the contact email in Info model
        )
    return render(request, 'contact/contact.html', {'myinfo': myinfo})
