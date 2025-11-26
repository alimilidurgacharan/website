from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import re

@api_view(['post'])
def send_contact_details(request):
    try:
        name = request.data.get("name")
        email = request.data.get("email")
        number = request.data.get("number")

        if not all([name, email, number]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):    
            return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST) 
        
        subject = "new Contact Form Submission"
        message = f"""
        Name: {name}
        Email: {email}
        Number: {number}
        """

        send_mail(
            subject = subject,
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [settings.RECIPIENT_EMAIL],
            fail_silently = False,
        )
        return Response({"message": "Contact details sent successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)