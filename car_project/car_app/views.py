from django.shortcuts import get_object_or_404, render,reverse, redirect
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Count
from datetime import datetime

from car_app.models import *


def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  
            messages.success(request, "Login successful!")
            return redirect('appointment_list')  
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def appointment_form(request):
    mechanics = Mechanic.objects.all()
    context = {
        'mechanics': mechanics
    }
    return render(request, 'appointment_form.html',context)

def appointment_list(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments,
    }
    return render(request, 'appointment_list.html', context)

@csrf_exempt  
@require_POST
def register_submit(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return JsonResponse({'success': False, 'error': 'Username and password are required.'})

    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'Username already exists.'})

    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({'success': True, 'redirect_url': reverse('login')})  
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def check_mechanic_availability(request):
    if request.method == "POST":
        mechanic_id = request.POST.get("mechanic_id")
        appointment_date = request.POST.get("appointment_date")

        count = Appointment.objects.filter(
            mechanic_id=mechanic_id,
            appointment_date=appointment_date
        ).count()

        if count >= 4:
            return JsonResponse({"available": False, "count": count})
        return JsonResponse({"available": True, "count": count})
      
@csrf_exempt
def submit_appointment(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."})

    try:
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")  
        car_license = request.POST.get("license")
        engine = request.POST.get("engine")
        mechanic_id = request.POST.get("mechanic")
        date_str = request.POST.get("date")

        if not all([name, address, phone, car_license, engine, mechanic_id, date_str]):
            return JsonResponse({"success": False, "error": "All fields are required."})

        appointment_date = parse_date(date_str)

        if Appointment.objects.filter(car_license=car_license, appointment_date=appointment_date).exists():
            return JsonResponse({
                "success": False,
                "error": f"An appointment already exists for this car license on {appointment_date}."
            })
        
        client, _ = Client.objects.get_or_create(
            car_license=car_license,
            defaults={
                "name": name,
                "email": email,
                "address": address,
                "phone": phone,
                "car_engine_number": engine
            }
        )
        Appointment.objects.create(
            appointment_date=appointment_date,
            mechanic_id=mechanic_id,
            car_license=car_license
        )

        return JsonResponse({"success": True, "message": "Appointment booked successfully.","redirect_url": "/appointment_list/"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def update_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    mechanics = Mechanic.objects.all()

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        mechanic_id = request.POST.get('mechanic')
        if appointment_date and mechanic_id:
            appointment.appointment_date = appointment_date
            appointment.mechanic = get_object_or_404(Mechanic, id=mechanic_id)
            appointment.save()
            return redirect('appointment_list')

    return render(request, 'update_appointment.html', {
        'appointment': appointment,
        'mechanics': mechanics
    })


def get_available_mechanics(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'mechanics': []})
    
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'mechanics': []})
    
    appointments_on_date = Appointment.objects.filter(appointment_date=selected_date)
    mechanics_with_counts = appointments_on_date.values('mechanic').annotate(appointment_count=Count('id'))

    busy_mechanic_ids = [m['mechanic'] for m in mechanics_with_counts if m['appointment_count'] >= 4]
    available_mechanics = Mechanic.objects.exclude(id__in=busy_mechanic_ids)
    mechanic_list = [{'id': m.id, 'name': m.name} for m in available_mechanics]
    return JsonResponse({'mechanics': mechanic_list})

def mechanic_list(request):
    mechanics = Mechanic.objects.all()
    context = {
        'mechanics': mechanics,
    }
    return render(request, 'mechanic_list.html', context)

def client_list(request):
    clients = Client.objects.order_by('car_license').distinct('car_license')
    context = {
        'clients': clients,
    }
    return render(request, 'client_list.html', context)


