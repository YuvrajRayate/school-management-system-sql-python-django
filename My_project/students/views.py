from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# ---------- SESSION CHECK ----------
def auth_required(request):
    if not request.session.get('user_id'):
        return False
    return True

# ---------- LOGIN ----------
def login_view(request):
    if request.method == "POST":
        # Look for user in your 'users' table
        user = AppUser.objects.filter(
            username=request.POST['username'],
            password=request.POST['password']
        ).first()

        if user:
            request.session['user_id'] = user.id
            request.session['role'] = user.role
            return redirect('dashboard')

    return render(request, 'students/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

# ---------- DASHBOARD ----------
def dashboard(request):
    if not auth_required(request):
        return redirect('login')
    return render(request, 'students/dashboard.html')

# ================= STUDENTS =================
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Student

def student_list(request):
    # Assuming auth_required is defined elsewhere in your project
    if not auth_required(request):
        return redirect('login')

    # 1. Get the search term from the URL (e.g., ?q=rahul)
    q = request.GET.get('q', '').strip() 

    # 2. Start with all students
    students_qs = Student.objects.all().order_by('id')

    # 3. Filter if a search exists
    if q:
        students_qs = students_qs.filter(student_name__icontains=q)

    # 4. Paginate the (potentially filtered) list
    paginator = Paginator(students_qs, 5) # Show 5 per page
    page_number = request.GET.get('page')
    students_obj = paginator.get_page(page_number)

    return render(request, 'students/students/list.html', {
        'students': students_obj,
        'q': q,  # We call it 'q' here so the HTML can find it
    })

def student_add(request):
    if not auth_required(request): 
        return redirect('login')

    if request.method == "POST":
        Student.objects.create(
            student_name=request.POST['student_name'],
            roll_no=request.POST['roll_no'],
            school_class_id=request.POST.get('school_class'),
            division_id=request.POST.get('division'),
            profile_pic=request.FILES.get('profile_pic') # Handles the image
        )
        return redirect('student_list')

    # THIS LINE BELOW IS WHAT WAS MISSING OR MISALIGNED
    # It must be outside the "if" block so the page shows up when you first click the button
    return render(request, 'students/students/add.html', {
        'classes': SchoolClass.objects.all(),
        'divisions': Division.objects.all()
    })
def student_edit(request, id):
    if not auth_required(request): 
        return redirect('login')
    
    student = get_object_or_404(Student, id=id)
    
    if request.method == "POST":
        student.student_name = request.POST['student_name']
        student.roll_no = request.POST['roll_no']
        student.school_class_id = request.POST.get('school_class')
        student.division_id = request.POST.get('division')
        
        # Check if a new image was uploaded
        if request.FILES.get('profile_pic'):
            student.profile_pic = request.FILES.get('profile_pic')
            
        student.save()
        return redirect('student_list')

    # --- THIS PART WAS LIKELY MISSING OR MISALIGNED ---
    # This sends the data to your edit.html page when you click the button
    return render(request, 'students/students/edit.html', {
        'student': student,
        'classes': SchoolClass.objects.all(),
        'divisions': Division.objects.all()
    })
    
def student_delete(request, id):
    get_object_or_404(Student, id=id).delete()
    return redirect('student_list')

# ================= CLASSES =================
def class_list(request):
    if not auth_required(request): return redirect('login')
    return render(request, 'students/classes/list.html', {'classes': SchoolClass.objects.all()})

def class_add(request):
    if request.method == "POST":
        SchoolClass.objects.create(class_name=request.POST['class_name'])
        return redirect('class_list')
    return render(request, 'students/classes/add.html')

def class_edit(request, id):
    cls = get_object_or_404(SchoolClass, id=id)
    if request.method == "POST":
        cls.class_name = request.POST['class_name']
        cls.save()
        return redirect('class_list')
    return render(request, 'students/classes/edit.html', {'cls': cls})

def class_delete(request, id):
    get_object_or_404(SchoolClass, id=id).delete()
    return redirect('class_list')

# ================= DIVISIONS =================
def division_list(request):
    if not auth_required(request): return redirect('login')
    return render(request, 'students/divisions/list.html', {'divisions': Division.objects.all()})

def division_add(request):
    if request.method == "POST":
        Division.objects.create(
            division_name=request.POST['division_name'],
            school_class_id=request.POST['school_class']
        )
        return redirect('division_list')
    return render(request, 'students/divisions/add.html', {'classes': SchoolClass.objects.all()})

def division_edit(request, id):
    division = get_object_or_404(Division, id=id)
    if request.method == "POST":
        division.division_name = request.POST['division_name']
        division.school_class_id = request.POST['school_class']
        division.save()
        return redirect('division_list')
    return render(request, 'students/divisions/edit.html', {
        'division': division,
        'classes': SchoolClass.objects.all()
    })

def division_delete(request, id):
    get_object_or_404(Division, id=id).delete()
    return redirect('division_list')