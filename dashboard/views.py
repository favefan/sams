from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db import models

from dashboard.models import User, Student, Activity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

login_page = 'dashboard/login.html'
account_manager_page = 'dashboard/account_manager.html'
index_page = 'dashboard/index.html'
name_or_pwd_error = 'Username or password error.'
user_already_exists = 'Username already exists.'
warning_null_value = 'Username or password not allow be null.'
sign_up_success = 'Sign up success! Please sign in.'

def log_in(request):
    if request.method == 'POST':
        if request.POST:
            username = request.POST['uname']
            password = request.POST['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #return render(request, centre_page)
                return HttpResponseRedirect(reverse('dashboard:index'))
            else:
                return render(request, login_page, {'info': name_or_pwd_error})
        else:
            return render(request, login_page, {'info': warning_null_value})
    else:
        return render(request, login_page)

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('dashboard:login'))

@login_required
def index(request):
    # part_acts_list = []
    # current_user = Student.objects.get(user=request.user)
    # entry_list = Entrylist.objects.filter(student=current_user)
    # for entry in entry_list:
    #     part_acts_list.append(entry.activity)
    # acts_list = Activity.objects.all()
    acts_list = []
    part_acts_list = []
    return render(request, 'dashboard/index.html', { 'acts_list': acts_list, 'part_acts_list': part_acts_list })

@login_required
def stu_manager(request):
    stus_list = Student.objects.all()
    return render(request, 'dashboard/stu_manager.html', { 'stus_list': stus_list })

@login_required
def account_manager(request):
    accounts_list = User.objects.all()
    return render(request, 'dashboard/account_manager.html', { 'accounts_list': accounts_list })

@login_required
def act_manager(request):
    organizer = User.objects.get(id=request.session.get('_auth_user_id'))
    mine_acts_list = Activity.objects.filter(organizer=organizer)
    return render(request, 'dashboard/act_manager.html', { 'mine_acts_list': mine_acts_list })

@login_required
def create_student(request):
    if request.POST:
        stu_id = request.POST['stu_id']
        stu_name = request.POST['stu_name']
        sex = request.POST['sex']
        depart = request.POST['depart']
        major = request.POST['major']
        en_year = request.POST['en_year']
        school_year = request.POST['school_year']
        username = stu_id
        password = None
        if len(stu_id) >= 6:
            password = stu_id[-6:]
        else:
            password = stu_id
        if Student.objects.filter(student_ID=stu_id).exists():
            return HttpResponse('输入的学号已存在，请检查.')
        else:
            student = Student(\
                student_ID=int(stu_id),\
                    name=stu_name,\
                        sex=int(sex),\
                            department=int(depart),\
                                major=major,\
                                    enroll_year=int(en_year),\
                                        schooling_year=int(school_year)\
                                            )
            if User.objects.filter(username=stu_id).exists():
                student.account_status = '账户冲突'
                student.save()
                return HttpResponse('学生信息创建成功, 但学生账户已经存在，无法关联账号，请检查。')
            else:
                student.save()
                new_user = User.objects.create_user(username=username, password=password, first_name=stu_name, account=student)
                new_user.save()  
                student.account_status = '已创建'
                student.save()
            return HttpResponse('学生信息创建成功，学生账户默认用户名为学号，默认密码为学号至少倒数六位。')
            #return render(request, centre_page, {'result_for_cs': 'Student and login account create success.username is: ' + username + ' , and password is: ' + password })
        #return render(request, centre_page, { 'result': [stu_id, stu_name, sex, depart, major, en_year, school_year] })

@login_required
def create_account(request):
    if request.method == 'POST':
        if request.POST:
            username = request.POST['uname']
            password = request.POST['pwd']
            if User.objects.filter(username=username).exists():
                return render(request, account_manager_page, {'info': user_already_exists})
            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                #return render(request, sign_in_page, {'info': sign_up_success})
                return HttpResponse('账户创建成功.')
        else:
            return HttpResponse(warning_null_value)
    else:
        return render(request, account_manager_page)

@login_required
def create_activity(request):
    if request.POST:
        act_name = request.POST['act_name']
        intro = request.POST['intro']
        organizer = User.objects.get(id=request.session.get('_auth_user_id')) 
        create_date = timezone.now()
        capacity = request.POST['capacity']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        # if Activity.objects.filter(name=act_name).exists():
        activity = Activity(\
            name=act_name,\
                introduction=intro,\
                    organizer=organizer,\
                        create_date=create_date,\
                            capacity=int(capacity),\
                                start_date=start_date,\
                                    end_date=end_date\
                                        )
        activity.save()
        return HttpResponse('活动创建成功。')
    else:
        return HttpResponse('输入内容不能为空。')
    #return HttpResponseRedirect(reverse('dashboard:index'))
    #return render(request, centre_page, { 'result_for_ca': [act_name, intro, organizer, create_date, capacity, start_date, end_date]})
    
@login_required
def delete_activity(request, activity_ID):
    act = Activity.objects.filter(activity_ID=activity_ID)
    if act.exists():
        act.delete()
    return HttpResponseRedirect(reverse('dashboard:index'))

@login_required
def delete_student(request, student_ID):
    stu = Student.objects.filter(student_ID=student_ID)
    stu_account = User.objects.filter(account=stu[0])
    if stu.exists():
        stu.delete()
        if stu_account.exists():
            stu_account.delete()
    return HttpResponseRedirect(reverse('dashboard:stu_manager'))

@login_required
def delete_account(request, account_ID):
    account = User.objects.filter(id=account_ID)
    if account.exists():
        if account[0].account:
            return HttpResponse('此账号关联了学生对象，无法删除，若要删除请删除对应学生对象。')
        else:
            account.delete()
            return HttpResponseRedirect(reverse('dashboard:account_manager'))


