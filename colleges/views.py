from django.shortcuts import render,redirect,get_object_or_404
from .models import Colleges
from django.contrib import messages
# Create your views here.
def colleges_login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            colleges = Colleges.objects.get(email=email)
            if colleges.check_password(password):
                request.session['college_id']=colleges.college_id
                request.session['college_name']=colleges.name
                return redirect('college_homepage')
            else:
                messages.error(request,"invalid email or password")
        except colleges.DoesNotExist:
            messages.error(request,"college with this email does not exist")

    return render(request,'colleges/colleges_login.html')

def colleges_signup(request):
    if request.method=='POST':
        name = request.POST['name']
        address = request.POST['address']
        contactno = request.POST['contact_no']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirm_password']

        if password != confirmpassword:
            messages.error(request,"passwords do not match")
            return render(request,'colleges/colleges_signup.html')

        colleges = Colleges(name=name,address=address,contactno=contactno,email=email,password=password)
        colleges.set_password(password)
        colleges.save()
        messages.success(request,"your account has been created succesfully")
        return redirect(colleges_login)
        
    return render(request,'colleges/colleges_signup.html')

def college_homepage(request):

    return render(request,'colleges/college_homepage.html')