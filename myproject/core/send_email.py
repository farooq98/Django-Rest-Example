from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from email_validator import validate_email, EmailNotValidError
from myapp.models import TestModel

def test_email(emails):
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

def send_verfication_email(email, code, purpose="email verification"):
    if settings.DEBUG:
        subject = f'{purpose.title()} From localhost'
    else:
        subject = f'{purpose.title()} From {settings.ALLOWED_HOSTS[0]}'
    
    if purpose == "email verification":
        message = f"We are excited to have you get started. First, you need to confirm your account. Your activation code is {code}"
    else:
        message = f"We have received a password reset request for your account. Please, verify the equest using the code {code}"
    email_from = settings.EMAIL_HOST_USER
    validated_emails = email_validation(email)

    if isinstance(validated_emails, EmailNotValidError) or \
       isinstance(validated_emails, ValueError):
        raise Exception(str(validated_emails))

    recipient_list = validated_emails[:1]

    html_message = loader.render_to_string(
                'user_registration/email_template.html',
                {
                    'message': message,
                    'activation_code':  code
                }
            )

    if settings.DEBUG:
        send_mail( subject, message, email_from, recipient_list )
    else:
        send_mail( subject, message, email_from, recipient_list, fail_silently=True, html_message=html_message )

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