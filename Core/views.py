from django.shortcuts import render, redirect
from .models import Center, Student, Coordinator
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashbord')
        else:
            error = 'Invalid credentials. Please try again.'
    else:
        error = None
    return render(request, 'login.html', {'error': error})

def logout(request):
    logout(request)
    return redirect('home')


def dashbord(request):
    return render(request, 'dashbord.html')

def coordinator_list(request):
    coordinators = Coordinator.objects.all()
    return render(request, 'coordinator_lists.html', {'coordinators': coordinators})


def add_coordinator(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        center1_id = request.POST['center1']
        center2_id = request.POST['center2']
        primary_mobile = request.POST['primary_mobile']
        secondary_mobile = request.POST['secondary_mobile']
        place = request.POST['place']
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            center1 = get_object_or_404(Center, id=center1_id)
            center2 = get_object_or_404(Center, id=center2_id)
            coordinator = Coordinator.objects.create(user=user, primary_mobile=primary_mobile, secondary_mobile=secondary_mobile, place=place)
            coordinator.centers.add(center1, center2)
            return redirect('coordinator_lists')
        except IntegrityError:
            message = f"The username '{username}' is already taken. Please choose a different username."
            centers = Center.objects.all()
            return render(request, 'add_coordinator.html', {'centers': centers, 'message': message})
    else:
        centers = Center.objects.all()
        return render(request, 'add_coordinator.html', {'centers': centers})
    
def edit_coordinator(request, coordinator_id):
    coordinator = get_object_or_404(Coordinator, id=coordinator_id)
    if request.method == 'POST':
        # Get the updated values from the form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        center1_id = request.POST['center1']
        center2_id = request.POST['center2']
        primary_mobile = request.POST['primary_mobile']
        secondary_mobile = request.POST['secondary_mobile']
        place = request.POST['place']
        
        try:
            # Update the user object
            user = coordinator.user
            user.username = username
            user.email = email
            if password:
                user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            # Update the coordinator object
            coordinator.primary_mobile = primary_mobile
            coordinator.secondary_mobile = secondary_mobile
            coordinator.place = place
            
            # Clear the existing centers and add the updated ones
            coordinator.centers.clear()
            center1 = get_object_or_404(Center, id=center1_id)
            center2 = get_object_or_404(Center, id=center2_id)
            coordinator.centers.add(center1, center2)
            coordinator.save()
            
            # Redirect to the coordinator list page
            return redirect('coordinator_lists')
        except IntegrityError:
            message = f"The username '{username}' is already taken. Please choose a different username."
            centers = Center.objects.all()
            return render(request, 'edit_coordinator.html', {'coordinator': coordinator, 'centers': centers, 'message': message})
    else:
        centers = Center.objects.all()
        return render(request, 'edit_coordinator.html', {'coordinator': coordinator, 'centers': centers})




def delete_coordinator(request, coordinator_id):
    coordinator = get_object_or_404(Coordinator, id=coordinator_id)
    coordinator.delete()
    return JsonResponse({'status': 'success'})


def center_list(request):
    centers = Center.objects.annotate(student_count=Count('student'))
    return render(request, 'center_list.html', {'centers': centers})


def center_add(request):
    if request.method == 'POST':
        ref_number = request.POST['ref_number']
        name = request.POST['name']
        location = request.POST['location']
        address = request.POST['address']
        center = Center(ref_number=ref_number, name=name, location=location, address=address)
        center.save()
        return redirect('center_list')
    return render(request, 'center_add.html')


def center_edit(request, center_id):
    center = Center.objects.get(pk=center_id)
    if request.method == 'POST':
        ref_number = request.POST['ref_number']
        name = request.POST['name']
        location = request.POST['location']
        address = request.POST['address']
        center.ref_number = ref_number
        center.name = name
        center.location = location
        center.address = address
        center.save()
        return redirect('center_list')
    return render(request, 'center_edit.html', {'center': center})


def center_delete(request, center_id):
    center = Center.objects.get( pk=center_id)
    center.delete()
    return redirect('center_list')



def center_student_list(request, center_id):
    center = Center.objects.get(id=center_id)
    students = Student.objects.filter(center=center)
    return render(request, 'center_student_list.html', {'center': center, 'students': students})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html' ,{'students':students})


def add_student(request):
    message = None
    if request.method == 'POST':
        ref_number = request.POST['ref_number']
        full_name = request.POST['full_name']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        email = request.POST['email']
        date_of_birth = request.POST['date_of_birth']
        preferred_location = request.POST['preferred_location']
        street_address = request.POST['street_address']
        state = request.POST['state']
        phone_number = request.POST['phone_number']
        guardian_name = request.POST['guardian_name']
        guardian_phone_number = request.POST['guardian_phone_number']
        id_proof = request.FILES['id_proof']
        age_group = request.POST['age_group']
        mode_of_travel = request.POST['mode_of_travel']
        football_playing_position = request.POST['football_playing_position']
        center_id = request.POST['center']
        school_Name = request.POST['school_Name']
        school_Address = request.POST['school_Address']
        study_Standard = request.POST['study_Standard']
        study_Devision  = request.POST['study_Devision']
        

        center = Center.objects.get(id=center_id)
        try:

            student = Student(ref_number=ref_number, full_name=full_name, city=city, zipcode=zipcode, email=email, date_of_birth=date_of_birth, 
                            preferred_location=preferred_location, street_address=street_address, state=state, phone_number=phone_number,
                            guardian_name=guardian_name, guardian_phone_number=guardian_phone_number, id_proof=id_proof, 
                            age_group=age_group, mode_of_travel=mode_of_travel, football_playing_position=football_playing_position,
                            center=center, school_Name=school_Name, school_Address=school_Address, study_Standard=study_Standard, study_Devision=study_Devision )
            student.save()
            return redirect('center_student_list', center_id=center.id)
        except IntegrityError:
            message = f"A student with this reference number already exists."
    centers = Center.objects.all()
    return render(request, 'add_student.html', {'centers': centers, 'message':message})



def add_student_tow(request):
    message = None
    if request.method == 'POST':
        ref_number = request.POST['ref_number']
        full_name = request.POST['full_name']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        email = request.POST['email']
        date_of_birth = request.POST['date_of_birth']
        preferred_location = request.POST['preferred_location']
        street_address = request.POST['street_address']
        state = request.POST['state']
        phone_number = request.POST['phone_number']
        guardian_name = request.POST['guardian_name']
        guardian_phone_number = request.POST['guardian_phone_number']
        id_proof = request.FILES['id_proof']
        age_group = request.POST['age_group']
        mode_of_travel = request.POST['mode_of_travel']
        football_playing_position = request.POST['football_playing_position']
        center_id = request.POST['center']
        school_Name = request.POST['school_Name']
        school_Address = request.POST['school_Address']
        study_Standard = request.POST['study_Standard']
        study_Devision  = request.POST['study_Devision']
        

        center = Center.objects.get(id=center_id)
        try:

            student = Student(ref_number=ref_number, full_name=full_name, city=city, zipcode=zipcode, email=email, date_of_birth=date_of_birth, 
                            preferred_location=preferred_location, street_address=street_address, state=state, phone_number=phone_number,
                            guardian_name=guardian_name, guardian_phone_number=guardian_phone_number, id_proof=id_proof, 
                            age_group=age_group, mode_of_travel=mode_of_travel, football_playing_position=football_playing_position,
                            center=center, school_Name=school_Name, school_Address=school_Address, study_Standard=study_Standard, study_Devision=study_Devision )
            student.save()
            return redirect('student_list')
        except IntegrityError:
            message = f"A student with this reference number already exists."
    centers = Center.objects.all()
    return render(request, 'add_student_tow.html', {'centers': centers, 'message':message})


def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students':students})



def update_student(request, student_id):
    student = Student.objects.get(id=student_id)
    message = None
    if request.method == 'POST':
        student.ref_number = request.POST['ref_number']
        student.full_name = request.POST['full_name']
        student.city = request.POST['city']
        student.zipcode = request.POST['zipcode']
        student.email = request.POST['email']
        student.date_of_birth = request.POST['date_of_birth']
        student.preferred_location = request.POST['preferred_location']
        student.street_address = request.POST['street_address']
        student.state = request.POST['state']
        student.phone_number = request.POST['phone_number']
        student.guardian_name = request.POST['guardian_name']
        student.guardian_phone_number = request.POST['guardian_phone_number']
        if request.FILES.get('id_proof'):
            student.id_proof = request.FILES['id_proof']
        student.age_group = request.POST['age_group']
        student.mode_of_travel = request.POST['mode_of_travel']
        student.football_playing_position = request.POST['football_playing_position']
        center_id = request.POST['center']

        center = Center.objects.get(id=center_id)
        student.center = center

        try:
            student.save()
            return redirect('student_list')
        except IntegrityError:
            message = f"A student with this reference number already exists."
    centers = Center.objects.all()
    return render(request, 'add_student_tow.html', {'centers': centers, 'message':message})


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return JsonResponse({'status': 'success'})


