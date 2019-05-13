from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db import models

from dashboard.models import User, Student, Activity, Entrylist
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

login_page = 'dashboard/login.html'
account_manager_page = 'dashboard/account_manager.html'
index_page = 'dashboard/index.html'
name_or_pwd_error = '用户名或密码不正确'
user_already_exists = '用户名已存在'
warning_null_value = '用户名或密码不能为空'
sign_up_success = 'Sign up success! Please sign in.'

###Instrumental function
def get_or_create_group(group_name, codename_list):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        permissions = Permission.objects.filter(codename__in=codename_list)
        group = Group.objects.create(name=group_name)
        group.permissions.set(permissions)
        group.save()
    return group

def auto_red_html(message, red_url):
    return  message + \
            '<head>\
                <meta http-equiv="refresh" content="5;URL=' + red_url + '">\
            </head>\
            <body>\
                <p>5秒后自动跳转...<br>或点击\
                    <a href="' + red_url + '">此处</a>\
                直接跳转。</p>\
            </body>'
###

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
    part_acts_list = []
    current_user = request.user
    if current_user.account is None:
        return HttpResponseRedirect(reverse('dashboard:open_acts'))
    else:
        student = current_user.account
        mine_entry_list = Entrylist.objects.filter(student=student)
        if mine_entry_list.exists():
            for entry in mine_entry_list:
                part_acts_list.append(entry.activity)
        return render(request, 'dashboard/index.html', {'part_acts_list': part_acts_list })

@login_required
@permission_required('dashboard.add_student', raise_exception=True)
def stu_manager(request):
    stus_list = Student.objects.all()
    return render(request, 'dashboard/stu_manager.html', { 'stus_list': stus_list })

@login_required
@permission_required('dashboard.add_user', raise_exception=True)
def account_manager(request):
    accounts_list = User.objects.all()
    return render(request, 'dashboard/account_manager.html', { 'accounts_list': accounts_list })

@login_required
@permission_required('dashboard.add_activity', raise_exception=True)
def act_manager(request):
    organizer = User.objects.get(id=request.session.get('_auth_user_id'))
    mine_acts_list = Activity.objects.filter(organizer=organizer)
    return render(request, 'dashboard/act_manager.html', { 'mine_acts_list': mine_acts_list })

@login_required
def info_edit(request):
    return render(request, 'dashboard/info_edit.html')

@login_required
def open_acts(request):
    open_acts_list = Activity.objects.all()
    return render(request, 'dashboard/open_acts.html', { 'open_acts_list': open_acts_list })

@login_required
@permission_required('dashboard.add_student', raise_exception=True)
def create_student(request):
    codename_list = [ 
        'view_activity', 
        'add_entrylist', 
    ]
    normal_users_group = get_or_create_group('normal_users', codename_list)
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
                normal_users_group.user_set.add(new_user)
                student.account_status = '已创建'
                student.save()
            return HttpResponse('学生信息创建成功，学生账户默认用户名为学号，默认密码为学号至少倒数六位。')
            #return render(request, centre_page, {'result_for_cs': 'Student and login account create success.username is: ' + username + ' , and password is: ' + password })
        #return render(request, centre_page, { 'result': [stu_id, stu_name, sex, depart, major, en_year, school_year] })

@login_required
@permission_required('dashboard.add_user', raise_exception=True)
def create_account(request):
    # activity_admins_group = Group.objects.get_or_create(name='activity_admins', permissions=permissions)
    codename_list = [
        'add_activity', 
        'change_activity', 
        'view_activity', 
        'add_entrylist', 
        'change_entrylist', 
        'delete_entrylist', 
        'view_entrylist', 
        'view_student',
    ]
    activity_admins_group = get_or_create_group('activity_admins', codename_list)
    if request.method == 'POST':
        if request.POST:
            username = request.POST['uname']
            password = request.POST['pwd']
            if User.objects.filter(username=username).exists():
                return render(request, account_manager_page, {'info': user_already_exists})
            else:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                activity_admins_group.user_set.add(new_user)
                #return render(request, sign_in_page, {'info': sign_up_success})
                return HttpResponse('账户创建成功.')
        else:
            return HttpResponse(warning_null_value)
    else:
        return render(request, account_manager_page)

@login_required
@permission_required('dashboard.add_activity', raise_exception=True)
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
@permission_required('dashboard.delete_activity', raise_exception=True)
def delete_activity(request, activity_ID):
    act = Activity.objects.filter(activity_ID=activity_ID)
    if act.exists():
        act.delete()
    return HttpResponseRedirect(reverse('dashboard:index'))

@login_required
@permission_required('dashboard.delete_student', raise_exception=True)
def delete_student(request, student_ID):
    stu = Student.objects.filter(student_ID=student_ID)
    stu_account = User.objects.filter(account=stu[0])
    if stu.exists():
        stu.delete()
        if stu_account.exists():
            stu_account.delete()
    return HttpResponseRedirect(reverse('dashboard:stu_manager'))

@login_required
@permission_required('dashboard.delete_user', raise_exception=True)
def delete_account(request, account_ID):
    account = User.objects.filter(id=account_ID)
    if account.exists():
        if account[0].account:
            return HttpResponse('此账号关联了学生对象，无法删除，若要删除请删除对应学生对象。')
        else:
            account.delete()
            return HttpResponseRedirect(reverse('dashboard:account_manager'))

@login_required
def edit_account(request):
    account_id = request.POST['id']
    try:
        account = User.objects.get(id=account_id)
    except User.DoesNotExist:
        return HttpResponse('Ops!Fake id.')
    else:
        if 'first_name' in request.POST:
            first_name = request.POST['first_name']
            account.first_name = first_name
            account.save()
            return HttpResponse('姓名修改成功！')
        elif 'password' in request.POST:
            password = request.POST['password']
            account.set_password(password)
            account.save()
            return HttpResponse('密码修改成功！')
        else:
            return HttpResponse('Ops!Nothing be submitted.')

@login_required
def enroll(request, activity_ID):
    current_user = request.user
    activity = Activity.objects.get(activity_ID=activity_ID)
    student = current_user.account
    entry_check = Entrylist.objects.filter(student=student, activity=activity)
    if entry_check.exists():
        return HttpResponse(auto_red_html('你已经报名了，请不要重复报名', '/dashboard/open_acts/'))
    else:
        enroll_activity = Entrylist(student=student, activity=activity, entry_date=timezone.now())
        enroll_activity.save()
        return HttpResponseRedirect(reverse('dashboard:open_acts'))
    
        
    

    
    
