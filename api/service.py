from django.core.mail import EmailMessage


def send_email(email: str, confirmation_code: str):
    email = EmailMessage(
        'confirmation_code',
        'confirmation_code: ' + confirmation_code,
        to=[email],
        headers={'Message-ID': 'confirm'}
    )
    email.send()
