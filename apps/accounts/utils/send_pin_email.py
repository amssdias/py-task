import random

from settings.database import redis_connection
from settings.utils.send_email import send_email

def send_account_activation_pin_email(email) -> None:
    """
    Generate a random pin, store it on redis DB and send it to the user.
    """
    pin = "".join([str(random.randint(0, 9)) for _ in range(4)])

    try:
        redis_connection.set(email, pin)

        subject = "Py-task - Activate your account"
        message = f"Your pin to activate your account is: {pin}"
        send_email(receiver=email, subject=subject, body=message)
    except Exception as e:
        # TODO: Logs
        pass
    
    return True
