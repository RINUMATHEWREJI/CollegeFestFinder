from django.shortcuts import render, redirect, get_object_or_404
from .models import Colleges, Event
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404

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

def delete_event_page(request, event_id=None):
    if 'college_id' in request.session:
        college_id = request.session['college_id']
        college = get_object_or_404(Colleges, pk=college_id)

        if event_id:
            try:
                event = Event.objects.get(pk=event_id, college=college)
            except Event.DoesNotExist:
                raise Http404("No Event matches the given query for this college.")

            if request.method == 'POST':
                event.delete()
                messages.success(request, "Event has been deleted successfully.")
                return redirect('colleges:delete_event_page_without_id')

        events = Event.objects.filter(college=college)
        return render(request, 'colleges/delete_event_page.html', {'events': events})

    return redirect('colleges:colleges_login')

def update_event_page(request):
    if 'college_id' in request.session:
        college_id = request.session['college_id']
        college = get_object_or_404(Colleges, pk=college_id)
        events = Event.objects.filter(college=college)

        return render(request, 'colleges/update_event_page.html', {'events': events})

    return redirect('colleges:colleges_login')

def update_event(request, event_id):
    if 'college_id' in request.session:
        college_id = request.session['college_id']
        college = get_object_or_404(Colleges, pk=college_id)
        event = get_object_or_404(Event, pk=event_id, college=college)

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
                event.event_date = event_date  # Should be in 'YYYY-MM-DD' format
                event.event_end_date = event_end_date  # Should be in 'YYYY-MM-DD' format
                event.event_venue = event_venue
                event.event_description = event_description
                event.event_status = event_status

                if event_logo:
                    event.event_logo = event_logo

                event.save()
                messages.success(request, "Event has been updated successfully.")
                return redirect('colleges:update_event_page')  # Redirect to update_event_page

        return render(request, 'colleges/update_event.html', {'event': event})

    return redirect('colleges:colleges_login')



def colleges_logout(request):
    request.session.flush()
    return redirect('students:homepage')