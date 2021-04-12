from django.urls import path
from . import views, HodViews, StudentViews
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.logins, name='login'),
   ## path('accounts/', include('django.contrib.auth.urls')),
    path('signup_admin', views.signup_admin, name="signup_admin"),
    path('signup_student', views.signup_student, name="signup_student"),
    path('do_admin_signup', views.do_admin_signup, name="do_admin_signup"),
    path('dl', views.dl, name='dl'),
    path('det', views.det),
    path('logout_user', views.logout_user),
    path('admin_home', HodViews.admin_home, name="admin_home"),
    path('add_students', HodViews.add_students),
    path('add_course', HodViews.add_course),
    path('add_course_save', HodViews.add_course_save),
    path('add_student_save', HodViews.add_student_save),
    path('manage_student', HodViews.manage_student),
    path('edit_student/<str:student_id>', HodViews.edit_student),
    path('edit_student_save', HodViews.edit_student_save),
    path('sending_notification/<int:pk>', HodViews.sending_notification, name='sending_notification'),
    path('save_notification', HodViews.save_notification, name='save_notification'),
    path('see_notification_admin', HodViews.see_notification_admin, name='see_notification_admin'),
    path('details_notification/<int:pk>', HodViews.details_notification, name='details_notification'),
    path('notify_details/<int:pk>', HodViews.notify_details, name='notify_details'),

    ##student url
    path('student_home', StudentViews.student_home, name="student_home"),
    path('details_notification_student/<int:pk>', StudentViews.details_notification_student, name="details_notification_student"),
    path('notify_details_student/<int:pk>', StudentViews.notify_details_student, name='notify_details_student'),

    #password reset
    path('password_reset/',views.PasswordReset,name='password_reset'),
    path('reset_password_email',views.reset_password_email,name='reset_password_email'),
    path('reset_password_email_done',views.reset_password_email_done,name='reset_password_email_done'),


]
