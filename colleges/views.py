from django.shortcuts import render, redirect, get_object_or_404
from .models import Colleges, Event,Feedback
from django.contrib import messages
from datetime import date
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
    
    if 'college_id'  in request.session:
        college_id = request.session['college_id']
        college = Colleges.objects.get(college_id=college_id)

        events = Event.objects.filter(college=college)

        event_feedbacks = []
        for event in events:
            feedbacks = Feedback.objects.filter(event=event)
            event_feedbacks.append({'event': event, 'feedbacks': feedbacks})

        return render(request,'colleges/college_homepage.html',{ 'event_feedbacks': event_feedbacks,'college_name':college.name})
    else:
        return redirect('colleges:colleges_login')
    
def add_event(request):
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
        event_pdf = request.FILES.get('event_pdf')

        # Parse the event start and end dates
        event_start_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        event_end_date = datetime.strptime(event_end_date_str, '%Y-%m-%d').date()

        # Set event status if the end date is in the past
        if event_end_date < datetime.now().date():
            event_status = 'closed'

        college = Colleges.objects.get(pk=request.session['college_id'])

        # Check for overlapping events only with other colleges
        overlapping_event = Event.objects.filter(
            event_start_date__lte=event_end_date,
            event_end_date__gte=event_start_date
        ).exclude(college=college).first()  # Exclude events from the same college

        if overlapping_event:
            # Correct the college reference in the error message
            messages.error(request, f"Another event '{overlapping_event.event_name}' from '{overlapping_event.college.name}' is already scheduled during this time.")
            return render(request, 'colleges/add_event.html')  # Re-render the form with error message

        # If no overlap, create and save the event
        event = Event(
            college=college,
            event_name=event_name,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            event_venue=event_venue,
            event_description=event_description,
            event_status=event_status
        )

        # Assign uploaded files if provided
        if event_logo:
            event.event_logo = event_logo

        if event_pdf:
            event.event_pdf = event_pdf

        event.save()  # Save the event to the database
        return redirect('colleges:college_homepage')  # Redirect to the college homepage after saving

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

            # Check if all required fields are filled
            if event_name and event_date and event_end_date and event_venue and event_description and event_status:
                event.event_name = event_name
                event.event_start_date = datetime.strptime(event_date, '%Y-%m-%d').date()  # Convert string to date
                event.event_end_date = datetime.strptime(event_end_date, '%Y-%m-%d').date()  # Convert string to date
                event.event_venue = event_venue
                event.event_description = event_description
                today = date.today()

                if today > event.event_end_date:
                    event.event_status = 'closed'
                    messages.warning(request, "The event's registration has been automatically closed as the end date has passed.")
                else:
                    event.event_status = event_status

                if event_logo:
                    event.event_logo = event_logo

                # Check for overlapping events with different colleges
                overlapping_event = Event.objects.filter(
                    event_start_date__lte=event.event_end_date,
                    event_end_date__gte=event.event_start_date
                ).exclude(college=college).first()  # Exclude the same college's event

                if overlapping_event:
                    messages.error(request, f"Another event '{overlapping_event.event_name}' from '{overlapping_event.college.name}' is already scheduled during this time.")
                    return render(request, 'colleges/update_event.html', {'event': event})

                event.save()  # Save the updated event
                messages.success(request, "Event has been updated successfully.")
                return redirect('colleges:update_event_page')  # Redirect to the update event page

        return render(request, 'colleges/update_event.html', {'event': event})  # Render the update form

    return redirect('colleges:colleges_login')

def colleges_logout(request):
    request.session.flush()
    return redirect('students:homepage')


def check_and_close_expired_events():
    today = datetime.now().date()
    # Find events that have an end date in the past and are still 'open'
    expired_events = Event.objects.filter(event_end_date__lt=today, event_status='open')
    # Update the status of these events to 'closed'
    expired_events.update(event_status='closed')
