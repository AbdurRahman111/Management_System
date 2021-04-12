from django.shortcuts import render
from .models import Students, Courses, send_notification

def student_home(request):
    user = request.user.email
    print(user)
    get_student = Students.objects.get(student_email=user)

    context={'get_student':get_student}
    return render(request, "student_template/base_template.html", context)

def details_notification_student(request, pk):
    get_details_notification=Courses.objects.get(id=pk)
    get_send_notification=send_notification.objects.filter(course_name=get_details_notification).order_by('-id')

    context3={'get_send_notification':get_send_notification}
    return render(request, 'hod_template/see_notification_student.html', context3)


def notify_details_student(request, pk):
    get_notify_all = send_notification.objects.get(id=pk)
    context4 = {'get_notify_all': get_notify_all}
    return render(request, 'student_template/details_notification_student.html', context4)
