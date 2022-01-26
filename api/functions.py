import random, string
from user_agents import parse
from django.utils.timezone import now, timedelta

def token_generator(size):
    _OTP = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(size))
    return _OTP

def get_device_details(ua_string):
    user_agent = parse(ua_string)
    return str(user_agent)

def expiry_time_5():
    return now() + timedelta(minutes=5)

def expiry_time_60():
    return now() + timedelta(minutes=60)

def mask_email(email):
    return email.split('@')[0][0]+ '**********' + email.split('@')[0][-1] + '@' + email.split('@')[1]