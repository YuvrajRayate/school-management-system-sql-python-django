from django.db import models

class AppUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20)
    class Meta:
        db_table = 'users'
    def __str__(self):
        return self.username

class SchoolClass(models.Model):
    class_name = models.CharField(max_length=50)
    class Meta:
        db_table = 'classes'
    def __str__(self):
        return self.class_name

class Division(models.Model):
    division_name = models.CharField(max_length=50)
    # Mapping to your existing table
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, db_column='class_id', db_constraint=False)
    class Meta:
        db_table = 'divisions'
    def __str__(self):
        return self.division_name

class Student(models.Model):
    student_name = models.CharField(max_length=255)
    roll_no = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='student_pics/', null=True, blank=True)
    
    # Linked to 'class_id' in your screenshot
    school_class = models.ForeignKey(
        'SchoolClass', on_delete=models.SET_NULL, null=True, blank=True, 
        db_column='class_id', db_constraint=False
    )
    # Linked to 'division_id' in your screenshot
    division = models.ForeignKey(
        'Division', on_delete=models.SET_NULL, null=True, blank=True, 
        db_column='division_id', db_constraint=False
    )

    class Meta:
        db_table = 'students'

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    class Meta:
        db_table = 'subjects'

class Teacher(models.Model):
    teacher_name = models.CharField(max_length=100)
    email = models.EmailField()
    class Meta:
        db_table = 'teachers'

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_constraint=False)
    attendance_date = models.DateField()
    status = models.CharField(max_length=20)
    class Meta:
        db_table = 'attendance'
        
class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_constraint=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_constraint=False)
    # Comment out or remove the school_class line if it's not in your DB table
    # school_class = models.ForeignKey(SchoolClass, ...) 

    class Meta:
        db_table = 'teacher_subjects'