from django.core.mail import send_mail
from django.conf import settings
from email_validator import validate_email, EmailNotValidError
from .models import TestModel

def email(emails):
    messages = "\n".join(
        [message['message'] for message in TestModel.objects.all() \
        .values('message')]
    )
    
    if settings.DEBUG:
        subject = 'Messages From localhost'
    else:
        subject = f'Messages From {settings.ALLOWED_HOSTS[0]}' 
    
    message = f'Here are all the messages listed Below\n{messages}'
    email_from = settings.EMAIL_HOST_USER
    validated_emails = email_validation(emails)
    
    if isinstance(validated_emails, EmailNotValidError) or \
       isinstance(validated_emails, ValueError):
        raise Exception(str(validated_emails))
    recipient_list = validated_emails
    send_mail( subject, message, email_from, recipient_list )

def check_email(email):
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError as e:
        return e

def email_validation(email):
    send_to = []
    if isinstance(email, str):
        returned_val = check_email(email)
        return returned_val if isinstance(returned_val, EmailNotValidError) else [returned_val]
    
    elif isinstance(email, list):
        for em in email:
            if not isinstance(em, str):
                return ValueError(f"{em} is not a valid email address")
            
            returned_val = check_email(em)
            if isinstance(returned_val, EmailNotValidError):
                return returned_val
            else:
                send_to.append(returned_val)
        return send_to
    
    else:
        return ValueError(f"{email} is not a valid email address")