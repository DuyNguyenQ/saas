import stripe
from decouple import config

DEBUG = config("DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="", cast=str)

if "sk_test" in STRIPE_SECRET_KEY and not DEBUG:
    raise ValueError("Invalid stripe secret key for production")

stripe.api_key = STRIPE_SECRET_KEY

def create_customer(name="", email="", raw=False):
    response = stripe.Customer.create(
        name=name,
        email=email,
    )
    if raw:
        return response
    
    stripe_id = response.id
    return stripe_id
