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
    path('create_student/', views.create_student),
    path('create_account/', views.create_account),
    # path('create_activity/', views.create_activity),
    # path('delete_activity?id=<int:activity_ID>', views.delete_activity, name="delete_activity")
]