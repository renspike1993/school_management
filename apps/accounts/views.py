from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# -----------------------
# LOGIN
# -----------------------
def login_view(request):
    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("account")
        else:
            error = "Invalid email or password"

    return render(request, "auth/login.html", {"error": error})


# -----------------------
# LOGOUT
# -----------------------
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def account_view(request):
    return render(request, "auth/account.html", {
        "user": request.user
    })