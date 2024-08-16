from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Admin
# Create your views here.
def admin_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact_no = request.POST['contact_no']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'students/student_signup.html')
        
        admin = Admin(name=name,contactno=contact_no,email=email,password=password)
        admin.set_password(password)
        admin.save()
        messages.success(request, "Your account has been created successfully")
        return redirect(admin_login)
    return render(request,'adminapp/admin_signup.html')
def admin_login(request):

    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        try:
            admin = Admin.objects.get(email=email)
            if admin.check_password(password):
                request.session['admin_id']=admin.admin_id
                request.session['admin_name']=admin.name
                return redirect('admin_homepage')
            else:
                messages.error(request,"invalid email or password")
        except admin.DoesNotExist:
            messages.error(request,"user with this email does not exist")
    return render(request,'adminapp/admin_login.html')

def admin_homepage(request):

    return render(request,'adminapp/admin_homepage.html')