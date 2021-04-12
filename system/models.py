from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


# Create your models here.
class CustomUser(AbstractUser):
    user_type_data = ((1, "admin"), (2, "Students"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    admin_name=models.ForeignKey(CustomUser, on_delete=models.CharField)
    # admin_name=models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.course_name

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_email = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=255, default='')
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default="")
    admin_details = models.CharField(max_length=255, default='')
  ##  profile_pic = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance,created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Students.objects.create(admin=instance, course_id=Courses.objects.get(id=1),gender="")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.students.save()


class send_notification(models.Model):
    message_box=models.CharField(max_length=100000)
    course_name = models.ForeignKey(Courses, on_delete=models.CASCADE)
    link_box=models.CharField(max_length=1000)

    # uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateField(default=datetime.now(), blank=True)
