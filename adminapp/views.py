from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Admin
from colleges.models import Colleges,Event
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
        events = Event.objects.filter(college = college)
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
                event.event_date = event_date  # Should be in 'YYYY-MM-DD' format
                event.event_end_date = event_end_date  # Should be in 'YYYY-MM-DD' format
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