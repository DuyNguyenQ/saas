from django.shortcuts import render
from django.urls import reverse
from .models import SubscriptionPrice

def subscription_price_view(request, interval="month", *args, **kwargs):
    qs = SubscriptionPrice.objects.filter(
        featured=True
    )
    def get_obj_list(interval):
        obj = {
            "day": qs.filter(
                    interval="day"
                ),
            "week": qs.filter(
                    interval="week"
                ),
            "month": qs.filter(
                    interval="month"
                ),
            "year": qs.filter(
                    interval="year"
                ),
        }
        return obj.get(interval, [])
    
    url_path_name = "pricing_interval"
    day_url = reverse(url_path_name, kwargs={"interval": "day"})
    week_url = reverse(url_path_name, kwargs={"interval": "week"})
    month_url = reverse(url_path_name, kwargs={"interval": "month"})
    year_url = reverse(url_path_name, kwargs={"interval": "year"})

    context = {
        "page_title": "Pricing",
        "obj_list": get_obj_list(interval),
        "day_url": day_url,
        "week_url": week_url,
        "month_url": month_url,
        "year_url": year_url,
        "active": interval,

    }
    return render(request, "subscriptions/pricing.html", context)

