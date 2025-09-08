from django.shortcuts import render
from visits.models import PageVisit

def home_page_view(request):
    html_template = "home.html"
    qs = PageVisit.objects.all()
    my_context = {
        "page_title": "ABC",
        "qs":  qs,
        "num_visit": qs.count()

    }
    PageVisit.objects.create()
    return render(request, html_template, my_context)

