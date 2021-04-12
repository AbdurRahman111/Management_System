from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect

#for file upload
from django.core.files.storage import FileSystemStorage

from .models import CustomUser, Students, Courses, send_notification
from .forms import send_notify

def admin_home(request):
    return render(request, "hod_template/base_template.html")

def add_students(request):
    user = request.user
    courses = Courses.objects.filter(admin_name=user)
    return render(request, "hod_template/add_student_template.html", {"courses": courses})

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        admin_id = request.POST.get("admin_id")

        details_admin = CustomUser.objects.get(id=admin_id)
        admin_names=details_admin.email
        print(admin_names)



        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        student_email = email
        password = request.POST.get("password")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        search_email = CustomUser.objects.filter(email=email)
        print(search_email)

        if search_email:
            messages.error(request, "Email Adress Already Exist !!")
            return HttpResponseRedirect("/add_students")
        else:
            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,last_name=last_name, first_name=first_name, user_type=2)
                course_obj = Courses.objects.get(id=course_id)
                user.students.student_email=student_email
                user.students.course_id = course_obj
                user.students.gender = sex
                user.students.admin_details = admin_names
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect("/add_students")
            except:
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect("/add_students")

def manage_student(request):
    user = request.user.email
    print(user)
    students = Students.objects.filter(admin_details=user)
    return render(request, "hod_template/manage_student_template.html", {"students": students})

def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    return render(request, "hod_template/edit_student_template.html", {"student": student})

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.session.get("student_id")

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        sex = request.POST.get("sex")

        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            student = Students.objects.get(admin=student_id)
            student.gender = sex
            student.save()
            messages.success(request, "Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/" + student_id)

        except:
            messages.error(request, "Failed to Edit Student")
            return HttpResponseRedirect("/edit_student/" + student_id)


def add_course(request):
    user = request.user
    admin_get_course= Courses.objects.filter(admin_name=user)
    contxt1={'admin_get_course':admin_get_course}
    return render(request,"hod_template/add_course.html", contxt1)

def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        admin_name = request.POST.get("admin_name")
        print(admin_name)

        get_admin= CustomUser.objects.get(id=admin_name)
        print(get_admin)

        try:
            course_model = Courses(course_name=course, admin_name=get_admin)
            course_model.save()
            messages.success(request, "Successfully Created Group")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect("/add_course")


def sending_notification(request, pk):
    get_courses=Courses.objects.get(id=pk)
    get_admin_name=get_courses.admin_name


    form = send_notify(instance=get_courses)
    if request.method == 'POST':
        form = send_notify(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form)


            messages.success(request, 'Notification Has been Sent !!')
            return HttpResponseRedirect("/add_course")

    course_details = Courses.objects.get(id=pk)

    student_info = Students.objects.filter(course_id=course_details)
    student_info_count = Students.objects.filter(course_id=course_details).count()

    context2={'course_details':course_details, 'student_info':student_info, 'student_info_count':student_info_count, 'form':form}
    return render(request,"hod_template/sending_notification.html", context2)

def save_notification(request):
    message_box=request.POST.get('message_box')
    course_name=request.POST.get('course_name')
    get_course = Courses.objects.get(id=course_name)
    links=request.POST.get('links')

    # file_upload = request.FILES['file_upload'] if 'file_upload' in request.FILES else None
    #
    # if file_upload:
    #     # print(file_upload.name)
    #     # print(file_upload.size)
    #     fs = FileSystemStorage()
    #     filename = fs.save(file_upload.name, file_upload)
    #     url_file = fs.url(filename)
    # else:
    #     url_file = ''

    save_send_notification=send_notification(message_box=message_box, course_name=get_course, link_box=links)
    save_send_notification.save()
    messages.success(request, 'Successfully Send Notification !!')
    return HttpResponseRedirect("/add_course")



def see_notification_admin(request):
    user= request.user

    message_box=request.POST.get('message_box')
    links=request.POST.get('links')

    get_course_name = Courses.objects.filter(admin_name=user)

    context3={'get_course_name':get_course_name}
    return render(request, 'hod_template/see_notification_admin.html', context3)


def details_notification(request, pk):

    get_details_notification=Courses.objects.get(id=pk)
    get_send_notification=send_notification.objects.filter(course_name=get_details_notification).order_by('-id')

    context3={'get_send_notification':get_send_notification}
    return render(request, 'hod_template/see_notification_admin_2.html', context3)

def notify_details(request, pk):
    get_notify_all = send_notification.objects.get(id=pk)
    context4 = {'get_notify_all': get_notify_all}
    return render(request, 'hod_template/details_notification.html', context4)