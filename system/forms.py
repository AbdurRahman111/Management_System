from django.forms import ModelForm
from django import forms
from .models import send_notification, CustomUser

class send_notify(ModelForm):
    class Meta:
        model = send_notification
        fields = ['course_name', 'message_box', 'link_box']


class CustomUser_details(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['password']

