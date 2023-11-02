from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from .forms import NewUserForm,UpdateProfileForm
from store.models import Order
from store.views import MainStoreView



# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"Successfully Registered!!")
            return redirect(MainStoreView)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request ,
                   template_name="account-register.html",
                   context={"register_form" : form})

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(MainStoreView)
            else:
                messages.error(request,"Given Credentials Are INVALID!!")
        else:
            messages.error(request,"Given Credentials Are INVALID!!")
    form = AuthenticationForm()
    return render(request , "account-login.html",context={'login_form':form})

def DashbordView(request):
    user_qs = User.objects.get(id = request.user.id)
    order_qs = Order.objects.filter(customer = request.user)

    return render(request , "account-dashboard.html",context={'user':user_qs,'orders':order_qs})

def ProfileView(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(DashbordView)
    else:
        profile_form = UpdateProfileForm()
    return render(request, "account-profile.html",{'form':profile_form})

def logoutView(request):
    logout(request)
    messages.info(request,'Succussfully Logged out!')
    return redirect(MainStoreView)

def passwordEditView(request):
    if request == 'POST' :
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return redirect('passwordEditView')
        messages.error(request,'Invalid Password!')
    form = PasswordChangeForm(request.user)
    return render(request,'account-password.html',context={'form':form})