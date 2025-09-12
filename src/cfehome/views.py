from django.shortcuts import render
from visits.models import PageVisit
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

LOGIN_URL = settings.LOGIN_URL


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

VALID_CODE = "abc123"
@login_required(login_url=LOGIN_URL)
def pw_protect_view(request, *args, **kwargs):
    print(request.POST)
    is_allowed = request.session.get('protected_page_allowed', None)
    print(request.session.get('protected_page_allowed', None), type(request.session.get('protected_page_allowed', None)))
    if request.method == "POST":
        user_pw_sent = request.POST.get("code", None)
        if user_pw_sent==VALID_CODE:
            request.session["protected_page_allowed"] = True
    if is_allowed:
        return render(request, "home.html", {}) 
    return render(request, "protected/entry.html", {})


@login_required(login_url=LOGIN_URL)
def user_only_view(request, *args, **kwargs):
    return render(request, "protect/user_only_view.html", {})


@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, "protect/staff_only_view.html", {})



