from django.shortcuts import render
from django.views import View
from .models import *

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from.googlecalendarapi import main
from datetime import datetime, timedelta
import pytz
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
                return render(request, "patient-home.html", {"user": user})
            return redirect("Doctor-home")
        except:
            return redirect("account-login")
        return render(request, "doctor-home", {"user": user})

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfuly Logged  out" )
    return redirect('account-login')

@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreateBlogApiView(View):
    def get(self, request):
        try:
            user=request.user
            if user.user_type=="DOCTOR":
                return render(request, "doctor-blog.html")
        except:
            messages.error(request, {"User is Not Doctor"})
            return redirect("account-login")
        return redirect("account-login")

    def post(self, request):
        user=request.user
        try:
            user1=User.objects.get(email=request.user.email)
            title = request.POST['title']
            content = request.POST['content']
            image = request.FILES.get('image', "")
            summary = request.POST['summary']
            catergory = request.POST['catergory']
            blog =Blog(title=title, content=content, image=image, summary=summary, category=catergory, user=user1)
            blog.save()
            return redirect("Doctor-home")
        except:
            return render(request, "doctor-blog.html")
        return render(request, "doctor-blog.html")

@method_decorator(login_required(login_url='/login'), name='dispatch')
class ShowBlogApiView(ListView):
    model = Blog
    template_name = "list-blog.html"
    def get(self, request):
        user=request.user
        if user.user_type=="PATIENT":
            Blog=self.model.objects.all()
            list=[]
            for i in Blog:
                summary=str(i.summary)
                n = 15
                s = summary
                m=s[:n] + (s[n:], '...')[len(s) > n]
                list.append(m)
            try:
                zipq=zip(Blog, list)
                return render(request, self.template_name, {"object_list": zipq})
            except:
                return render(request, self.template_name)
        else:
            return redirect("account-login")

@method_decorator(login_required(login_url='/login'), name='dispatch')
class Draft(ListView):
    model = Draft
    template_name = "account/draf.html"

    def get(self, request):
        user = request.user
        if user.user_type == "DOCTOR":
            draft = self.model.objects.all()
            return render(request, self.template_name, {"object_list":draft})
        else:
            return redirect("account-login")
@method_decorator(login_required(login_url='/login'), name='dispatch')
class DoctorListApiView(ListView):
    model = User
    template_name = "doctordetails.py.html"

    def get(self, request):
        user = request.user
        if user.user_type == "PATIENT":
            draft = self.model.objects.all().filter(user_type="DOCTOR")
            print(draft)
            return render(request, self.template_name, {"object_list":draft})
        else:
            return redirect("account-login")
@method_decorator(login_required(login_url='/login'), name='dispatch')
class BookAppointmentApiView(View):
    def get(self, request, id):
        if request.user.user_type=="PATIENT":
            return render(request, "account/appointment.html", {"id": id})
        return redirect("account-login")

    def post(self, request, id):
        user=request.user
        useremail=user.email
        try:
            doctor = User.objects.get(id=id)
            required = request.POST['required']
            date = request.POST['date']
            main(doctor, useremail, required)
            start_datetime = datetime.now(tz=pytz.utc)
            starttime = start_datetime.isoformat()
            endtime = (start_datetime + timedelta(minutes=45)).isoformat()
            appointment = Appointment(start_time=start_datetime, end_time=endtime, specialization=required,
                                      customer=user,
                                      doctor=doctor)
            appointment.save()
            return render(request, "patient-home.html", {"user": user})
        except:
            return redirect("account-login")


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ShowAppointmentApiView(ListView):
    model = User
    template_name = 'showappointment.html'

    def get(self, request):
        if request.user.user_type=="PATIENT":
            try:
                draft = self.model.objects.get(id=request.user.id)
                data=draft.patient.all()
            except User.DoesNotExit:
                return redirect("account-login")
        else:
            return redirect("account-login")
        return render(request, self.template_name, {"object_list": data})





