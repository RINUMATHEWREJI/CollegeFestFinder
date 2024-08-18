from django.shortcuts import render, redirect, get_object_or_404
from .models import Colleges, Event
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required

def colleges_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            college = Colleges.objects.get(email=email)
            if college.check_password(password):
                request.session['college_id'] = college.college_id
                request.session['college_name'] = college.name
                return redirect('colleges:college_homepage')
            else:
                messages.error(request, "Invalid email or password")
        except Colleges.DoesNotExist:
            messages.error(request, "College with this email does not exist")

    return render(request, 'colleges/colleges_login.html')

def colleges_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        contactno = request.POST['contact_no']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirm_password']

        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return render(request, 'colleges/colleges_signup.html')

        college = Colleges(name=name, address=address, contactno=contactno, email=email)
        college.set_password(password)
        college.save()
        messages.success(request, "Your account has been created successfully")
        return redirect('colleges:colleges_login')

    return render(request, 'colleges/colleges_signup.html')

def college_homepage(request):
    # Ensure that only authenticated colleges can access this page
    if 'college_id'  in request.session:
        college_id = request.session['college_id']
        college = Colleges.objects.get(college_id=college_id)

        events = Event.objects.filter(college=college)

        return render(request,'colleges/college_homepage.html',{'events':events, 'college_name':college.name})
    else:
        return redirect('colleges:colleges_login')
    
def add_event(request):
    # Check if the user is logged in by checking the session
    if 'college_id' not in request.session:
        return redirect('colleges:colleges_login')

    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date_str = request.POST.get('event_date')
        event_end_date_str = request.POST.get('event_end_date')
        event_venue = request.POST.get('event_venue')
        event_description = request.POST.get('event_description')
        event_logo = request.FILES.get('event_logo')
        event_status = request.POST.get('event_status')

        event_date = parse_datetime(event_date_str)
        event_end_date = parse_datetime(event_end_date_str)

        # Retrieve the college object from the session
        college = Colleges.objects.get(pk=request.session['college_id'])

        event = Event(
            college=college,
            event_name=event_name,
            event_date=event_date,
            event_end_date=event_end_date,
            event_venue=event_venue,
            event_description=event_description,
            event_status=event_status
        )

        if event_logo:
            event.event_logo = event_logo

        event.save()
        return redirect('colleges:college_homepage')

    return render(request, 'colleges/add_event.html')
