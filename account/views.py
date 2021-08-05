from django.shortcuts import render
from django.views import View
from .models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
class AccountSignupApiView(View):
    def get(self, request):
        return render(request, "account/signup.html")

    def post(self,request):
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        image = request.FILES.get('image', "")
        address=request.POST['address']
        usertype=request.POST['usertype']
        countery=request.POST['country']
        state=request.POST['state']
        zip=request.POST['zip']
        try:
            user = User.objects.filter(email=email).exists()
            if pass1 != pass2:
                messages.error(request, 'Password do no match')
                return redirect('account-signup')
            myuser = User.objects.create_user(username, email, pass1, is_staff=True)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.email=email
            myuser.profilepicture=image
            myuser.address=address
            myuser.pincode=zip
            myuser.state=state
            myuser.country=countery
            myuser.user_type=usertype
            myuser.save()
            return redirect('account-login')
        except :
            messages.error(request, "Email is already exits")
            return redirect('account-signup')



class AccountLoginApiView(View):
    def get(self,request):
        return render(request, "account/login.html")

    def post(self, request):
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        try:
            user = authenticate(username=loginusername, password=loginpassword)
            login(request, user)
            if user.is_authenticated and user.user_type=="DOCTOR":
                return redirect("Doctor-home")
            if user.is_authenticated and user.user_type=="PATIENT":
                return redirect("Patient-home")

        except:
            messages.success(request, "Invaild  Credentials, Please try again")
            return redirect("account-login")
@method_decorator(login_required(login_url='/login'), name='dispatch')
class DoctorHomeApiView(View):
    def get(self, request):
        try:
            user=request.user
            if user.user_type=="DOCTOR":
                return render(request, "doctor-home.html", {"user":user})
            return redirect("Patient-home")
        except:
            return redirect("account-login")
        return render(request, "doctor-home", {"user": user})

@method_decorator(login_required(login_url='/login'), name='dispatch')
class PatinentHomeApiView(View):
    def get(self, request):
        try:
            user = request.user
            if user.user_type=="PATIENT":
                return render(request, "doctor-home.html", {"user": user})
            return redirect("Doctor-home")
        except:
            return redirect("account-login")
        return render(request, "doctor-home", {"user": user})
def handlelogout(request):
    logout(request)
    messages.success(request,"Successfuly Logged  out" )
    return redirect('account-login')