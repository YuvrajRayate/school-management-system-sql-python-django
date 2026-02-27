from django.contrib import admin
from .models import (
    SchoolClass,
    Division,
    Student,
    Subject,
    Teacher,
    TeacherSubject,
    Attendance,
   
)

admin.site.register(SchoolClass)
admin.site.register(Division)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(TeacherSubject)
admin.site.register(Attendance)

