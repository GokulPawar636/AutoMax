from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views import View
from . forms import UserForm, ProfileForm, LocationForm

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

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    
    def get(self,request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)
        return render(request, 'main/profile.html', {'user_form':user_form,
                                                     'profile_form':profile_form,
                                                     'location_form': location_form})
    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        location_form = LocationForm(
            request.POST, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error Updating Profile!')





