from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.apps import apps
from datetime import datetime

Admin = apps.get_model('adminapp', 'Admin')
Colleges = apps.get_model('colleges', 'Colleges')
Event = apps.get_model('colleges', 'Event')
Student = apps.get_model('students', 'Student')
Feedback = apps.get_model('colleges', 'Feedback')

# Create your views here.
def add_admin(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact_no = request.POST['contact_no']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'adminapp/add_admin.html')
        
        admin = Admin(name=name,contactno=contact_no,email=email,password=password)
        admin.set_password(password)
        admin.save()
        messages.success(request, "Your account has been created successfully")
        return redirect('adminapp:admin_login')
    return render(request,'adminapp/add_admin.html')

def admin_login(request):

    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        try:
            admin = Admin.objects.get(email=email)
            if admin.check_password(password):
                request.session['admin_id']=admin.admin_id
                request.session['admin_name']=admin.name
                return redirect('adminapp:admin_homepage')
            else:
                messages.error(request,"invalid email or password")
        except Admin.DoesNotExist:
            messages.error(request,"user with this email does not exist")
    return render(request,'adminapp/admin_login.html')

def admin_homepage(request):
    if 'admin_id' in request.session:
        admin_id = request.session['admin_id']

        colleges = Colleges.objects.all()
        return render(request,'adminapp/admin_homepage.html',{'colleges':colleges})
    
    else:
        return redirect('adminapp:admin_login')
    
def edit_events_page(request,college_id):
    if 'admin_id' in request.session:
        college = get_object_or_404(Colleges,college_id=college_id)
        events = Event.objects.filter(college = college).prefetch_related('feedbacks')
        return render(request,'adminapp/edit_events_page.html',{'events': events})
    else:
        return redirect('adminapp:admin_login')

def edit_events(request,event_id):
    if 'admin_id' in request.session:
        event = get_object_or_404(Event,event_id=event_id)
        if request.method == 'POST':
            event_name = request.POST.get('event_name')
            event_date = request.POST.get('event_date')
            event_end_date = request.POST.get('event_end_date')
            event_venue = request.POST.get('event_venue')
            event_description = request.POST.get('event_description')
            event_logo = request.FILES.get('event_logo')
            event_status = request.POST.get('event_status')

            if event_name and event_date and event_end_date and event_venue and event_description and event_status:
                event.event_name = event_name
                event.event_date = event_date  
                event.event_end_date = event_end_date  
                
                event.event_venue = event_venue
                event.event_description = event_description
                event.event_status = event_status

                if event_logo:
                    event.event_logo = event_logo

                event.save()
                messages.success(request, "Event has been updated successfully.")
                return redirect('adminapp:edit_events_page', college_id = event.college.college_id) 
        return render(request,'adminapp/edit_events.html',{'event':event , 'college_id': event.college.college_id})
    else:
        return redirect('adminapp:admin_login')

def delete_events(request,event_id):
    if 'admin_id' in request.session:
        event = get_object_or_404(Event, event_id=event_id)
        college_id = event.college.college_id
        event.delete()
        messages.success(request, 'Event deleted successfully')
        return redirect('adminapp:edit_events_page', college_id=college_id)
    else:
        return redirect('adminapp:admin_login')
    
def manage_students(request):

    if 'admin_id' in request.session:
        students = Student.objects.all()


        return render(request,'adminapp/manage_students.html',{'students':students})
    else:
        return redirect('adminapp:admin_login')


def add_student(request):
    if 'admin_id' in request.session:
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
                return render(request, 'adminapp/add_student.html')
        
            student = Student(name=name,age=age,collegename=collegename,branch=branch,year=year,contact_no=contact_no,dateofbirth=dateofbirth,email=email,password=password)
            student.set_password(password)
            student.save()
            messages.success(request, "Your account has been created successfully")
            return redirect('adminapp:manage_students')
        return render(request,'adminapp/add_student.html')
    else:
        return redirect('adminapp:admin_login')

def edit_student(request, student_id):
    if 'admin_id' in request.session:
        student = get_object_or_404(Student, pk=student_id)
        if request.method == "POST":
            name = request.POST['name']
            age = request.POST['age']
            collegename = request.POST['collegename']
            branch = request.POST['branch']
            year = request.POST['year']
            contact_no = request.POST['contact_no']
            email = request.POST['email']


            if name and age and collegename and branch and year and contact_no and email:
                student.name = name
                student.age = age
                student.collegename = collegename
                student.branch = branch
                student.year = year
                student.contact_no = contact_no
                student.email = email

                student.save()
                messages.success(request, "Student has been updated successfully.")
                return redirect('adminapp:manage_students')
        
        return render(request, 'adminapp/edit_student.html', {'student': student})
    else:
        return redirect('adminapp:admin_login')
    

def delete_student(request,student_id):
    if 'admin_id' in request.session:
        student = get_object_or_404(Student,student_id=student_id)
        student.delete()
        messages.success(request, "Student has been deleted successfully.")
        return redirect('adminapp:manage_students')
    else:
        return redirect('adminapp:admin_login')

def manage_colleges(request):

    if 'admin_id' in request.session:
        colleges = Colleges.objects.all()


        return render(request,'adminapp/manage_colleges.html',{'colleges':colleges})
    else:
        return redirect('adminapp:admin_login')
    
def add_colleges(request):
    if 'admin_id' in request.session:
        if request.method == 'POST':
            name = request.POST['name']
            address = request.POST['address']
            contactno = request.POST['contactno']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return render(request, 'adminapp/add_colleges.html')
        
            college = Colleges(name=name,address=address,contactno=contactno,email=email,password=password)
            college.set_password(password)
            college.save()
            messages.success(request, "Your account has been created successfully")
            return redirect('adminapp:manage_colleges')
        return render(request,'adminapp/add_colleges.html')
    else:
        return redirect('adminapp:admin_login')
    
def edit_colleges(request, college_id):
    if 'admin_id' in request.session:
        college = get_object_or_404(Colleges, pk=college_id)
        if request.method == "POST":
            name = request.POST['name']
            address = request.POST['address']
            contactno = request.POST['contactno']
            email = request.POST['email']


            if name and address and  contactno and email:
                college.name = name
                college.address = address
                college.contactno = contactno
                college.email = email

                college.save()
                messages.success(request, "College has been updated successfully.")
                return redirect('adminapp:manage_colleges')
        return render(request, 'adminapp/edit_colleges.html', {'college': college})
    else:
        return redirect('adminapp:admin_login')
    
def delete_colleges(request,college_id):
    if 'admin_id' in request.session:
        colleges = get_object_or_404(Colleges,college_id=college_id)
        colleges.delete()
        messages.success(request, "college has been deleted successfully.")
        return redirect('adminapp:manage_colleges')
    else:
        return redirect('adminapp:admin_login')
    
    
def delete_feedback(request, feedback_id):
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, feedback_id=feedback_id)
        college_id = feedback.event.college.college_id
        feedback.delete()
        return redirect('adminapp:edit_events_page',college_id=college_id)