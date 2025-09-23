from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def profile_list_view(request):
    context = {
        "obj_list": User.objects.filter(is_active=True),
        "page_title": "User",
    }
    return render(request, "profiles/list.html", context)


@login_required(login_url=settings.LOGIN_URL)
def profile_detail_view(request, username=None, *args, **kwargs):
    # user = User.objects.get(username=username)
    is_me = False
    # <app_label>.view_<model_name>
    profile_user_obj = get_object_or_404(User, username=username)
    user_groups = profile_user_obj.groups.all()
    print(user_groups)
    # if user_groups.filter(name__icontains='basic').exists():
        # return HttpResponse("Congrats")
    print("subscription" ,profile_user_obj.has_perm("subscriptions.advanced"))
    
    if request.user.id == profile_user_obj.id:
        is_me = True
    
    context = {
        "instance": profile_user_obj,
        "page_title": f"Profile_{profile_user_obj.username}",
        "is_me": is_me,
    }

    return render(request, 'profiles/detail.html', context)


@login_required(login_url=settings.LOGIN_URL)
def profile_me_view(request, *args, **kwargs):
    context = {
        "instance": request.user,
        "page_title": "Profile Me",
    }

    return render(request, 'profiles/me.html', context)
    

    
