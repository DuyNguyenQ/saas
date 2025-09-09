from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        
        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    return render(request, "auth/login.html", {})
   

def logout_view(request):
    logout(request)
    return redirect("/login/") 

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        password_again = request.POST.get("password_again", None)

        if all([username, email, password, password_again]):
            if password != password_again:
                return render(request, "auth/register.html")
            
            # user_exist_qs = User.objects.filter(username__iexact=username).exists()
            try:
                user = User.objects.create_user(email=email, username=username, password=password)
            except:
                pass
    return render(request, "auth/register.html")
