from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Student 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
# Create your views here.

def homepage(request):

    return render(request,'students/homepage.html')

def login_selection(request):
    return render(request,'students/login_selection.html')

def student_login(request):

    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        try:
            student = Student.objects.get(email=email)
            if student.check_password(password):
                request.session['student_id']=student.student_id
                request.session['student_name']=student.name
                return redirect('student_homepage')
            else:
                messages.error(request,"invalid email or password")
        except student.DoesNotExist:
            messages.error(request,"user with this email does not exist")

    return render(request,'students/student_login.html')

def student_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        collegename = request.POST['collegename']
        branch = request.POST['branch']
        year = request.POST['year']
        contact_no = request.POST['contact_no']
        dateofbirth = request.POST['dateofbirth']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'students/student_signup.html')
        
        student = Student(name=name,age=age,collegename=collegename,branch=branch,year=year,contact_no=contact_no,dateofbirth=dateofbirth,email=email,password=password)
        student.set_password(password)
        student.save()
        messages.success(request, "Your account has been created successfully")
        return redirect(student_login)

    return render(request,'students/student_signup.html')


def student_homepage(request):
    if 'student_id' in request.session:
        student_name = request.session['student_name']
        return render(request, 'students/student_homepage.html', {'student_name': student_name})
    else:
        return redirect('students/student_login')