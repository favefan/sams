from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out),
    path('index/', views.index, name='index'),
    path('stu_manager/', views.stu_manager, name='stu_manager'),
    path('account_manager/', views.account_manager, name='account_manager'),
    path('act_manager/', views.act_manager, name='act_manager'),
    path('create_student/', views.create_student),
    path('create_account/', views.create_account),
    path('create_activity/', views.create_activity),
    path('delete_student?id=<int:student_ID>', views.delete_student, name='delete_student'),
    path('delete_account?id=<int:account_ID>', views.delete_account, name='delete_account'),
    path('edit_account/', views.edit_account),
    path('info_edit/', views.info_edit, name="info_edit"),
    path('open_acts/', views.open_acts, name="open_acts"),
    path('enroll?act_id=<int:activity_ID>', views.enroll, name="enroll"),
    path('act_info?act_id=<int:activity_ID>', views.act_info, name="act_info"),
    path('edit_act?act_id=<int:activity_ID>', views.edit_act, name="edit_act"),
]