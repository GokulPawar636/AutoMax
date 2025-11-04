from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views import View

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate( username=username, password=password)
            if user is not None:
                login(request, user)  # ✅ Important: creates session
                messages.success(request, f"welcome {username}! now you are loged in")
                return redirect('home')
            else:
                messages.error(request, f'An error occurred. please try again')
        else:
            messages.error(request, f'Invalid username or password. please try again')
    elif request.method == "GET":
        form = AuthenticationForm()
    
    return render(request, "main/login.html", {"login_form": form})



def register_view(request):
    register_form = UserCreationForm()
    return render(request, "main/register.html",{"register_form": register_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('main')
      



class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "main/register.html", {"register_form": form})
    
    def post(self, request):
        register_form = UserCreationForm(request = request, data = request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_form_db()
            password = register_form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=password)
            login(request, user)
            messages.success(request,
                             f"User {user.username} registration successful.")
            return redirect("home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request, "main/register.html", {"register_form": register_form})  
        
 