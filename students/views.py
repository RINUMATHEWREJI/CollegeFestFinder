from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Student 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from colleges.models import Colleges,Event,EventRegistration
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
                return redirect('students:student_homepage')
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
        student_id = request.session['student_id']

        colleges = Colleges.objects.all()

        query = request.GET.get('search')
        if query:
            colleges = colleges.filter(name__icontains = query)

        registered_events = Event.objects.filter(eventregistration__student_id = student_id)
        return render(request, 'students/student_homepage.html', {'student_name': student_name , 'colleges':colleges , 'registered_events':registered_events})
    else:
        return redirect('students:student_login')
    

def view_college_events(request, college_id):
    college = get_object_or_404(Colleges, college_id=college_id)
    events = Event.objects.filter(college=college)
    return render(request, 'students/view_college_events.html', {'college': college,'events': events })

def register_for_event(request, event_id):
    if request.method == 'POST':
        if 'student_id' in request.session:
            student = get_object_or_404(Student, student_id=request.session['student_id'])
            event = get_object_or_404(Event, event_id=event_id)

            # Ensure the event is open before registering
            if event.event_status == 'open':
                # Check if the student is already registered for the event
                registration, created = EventRegistration.objects.get_or_create(student=student, event=event)
                
                if created:
                    # Registration was just created, so it's a success
                    messages.success(request, f'You have successfully registered for {event.event_name}!')
                else:
                    # Registration already exists
                    messages.info(request, f'You are already registered for {event.event_name}.')
            else:
                # The event is closed, so registration is not allowed
                messages.error(request, 'Registration for this event is closed.')

        # Redirect back to the list of events for the college
        return redirect('students:view_college_events', college_id=event.college.college_id)

def student_logout(request):
    request.session.flush()
    return redirect ('students:homepage')