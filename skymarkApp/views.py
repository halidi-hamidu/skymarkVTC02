from django.shortcuts import render
from select import select
from time import strftime
from turtle import update
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import ManageClass, ManageCourses
from .forms import *
from django.contrib import messages
import datetime
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template, render_to_string
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.conf.global_settings import LOGIN_URL

# Create your views here.

# loginPage


def loginPage(request):
    if request.method == "POST":
        get_username = request.POST.get("username")
        get_password = request.POST.get('password')
        user = authenticate(username=get_username, password=get_password)
        if user is not None:
            login(request, user)
            messages.success(request, f'successful Login as {user}')
            return redirect("skymarkApp:dashboardPage")
        else:
            messages.info(request, "Incorrect username or password")
            return redirect("skymarkApp:loginPage")
    else:
        template_name = 'skymarkPages/LoginPages/loginPage.html'
        context = {}
        return render(request, template_name, context)

# dashboardPage


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=LOGIN_URL)
def dashboardPage(request):
    if request.method == 'POST' and request.POST.get('student_is_present'):
        form = ManageStudentSAttendanceForm(request.POST)
        get_students_id = request.POST.get('student_name')
        get_students_full_name = ManageStudentDetails.objects.get(
            id=get_students_id)
        print("===========", get_students_full_name)
        if form.is_valid():
            ManageStudentDetails.objects.filter(
                id=get_students_id).update(today_attendence=True)
            instance = form.save(commit=False)
            instance.attendance_status = True
            instance.course_name = get_students_full_name.course_name
            instance.save()
            messages.success(
                request, f'Student {get_students_full_name} is present')
            return redirect('skymarkApp:dashboardPage')
        else:
            messages.info(
                request, f"please try again")
            return redirect('skymarkApp:dashboardPage')

    if request.method == 'POST' and request.POST.get('student_is_absent'):
        form = ManageStudentSAttendanceForm(request.POST)
        get_students_id = request.POST.get('student_name')
        get_students_full_name = ManageStudentDetails.objects.get(
            id=get_students_id)
        print("===========", get_students_full_name)
        if form.is_valid():
            ManageStudentDetails.objects.filter(
                id=get_students_id).update(today_attendence=False)

            instance = form.save(commit=False)
            instance.attendance_status = False
            instance.course_name = get_students_full_name.course_name
            instance.save()
            messages.success(
                request, f'Student {get_students_full_name} is absent')
            return redirect('skymarkApp:dashboardPage')
        else:
            messages.info(
                request, f"please try again")
            return redirect('skymarkApp:dashboardPage')

    # Obtain_Staff_permision_
    user = User.objects.get(username=request.user)
    get_staff = ManageStaffDetails.objects.get(username=user)
    try:
        get_staff_permision = ManageAccountPermision.objects.get(
            staff_full_name=get_staff)
    except:
        get_staff_permision = ManageAccountPermision.objects.filter(
            staff_full_name=get_staff)
    # obtain staff which course he_or_she teach
    staff_course_name = get_staff.class_name
    get_students_by_its_course = ManageStudentDetails.objects.filter(
        course_name=get_staff.class_name).count()

    # obtain_student_by_specific_course_acccording_to_staff_who_acccess_the_system
    get_course = ManageCourses.objects.get(course_name=staff_course_name)
    get_present_student_by_its_course = ManageStudentSAttendance.objects.filter(
        course_name=staff_course_name.id, attendance_status=True).count()

    get_absent_student_by_its_course = ManageStudentSAttendance.objects.filter(
        course_name=staff_course_name.id,  attendance_status=False).count()
    get_all_students_by_its_course = ManageStudentDetails.objects.filter(
        course_name=staff_course_name.id).order_by('-id')

    count_all_lessons = ManageLessonToughtAtCollege.objects.all().count()
    get_all_lessons = ManageLessonToughtAtCollege.objects.all().order_by('-created_at')
    count_all_students = ManageStudentDetails.objects.all().count()
    count_all_staff = ManageStaffDetails.objects.all().count()
    count_all_courses = ManageCourses.objects.all().count()
    today_date = datetime.datetime.today().date()
    curent_login_user_its_course = get_staff.class_name
    count_all_student_present_today = ManageStudentSAttendance.objects.filter(
        date=today_date, attendance_status=True).count()
    count_all_student_present_today_specific_class = ManageStudentSAttendance.objects.filter(
        date=today_date, attendance_status=True, course_name=curent_login_user_its_course).count()

    count_all_student_absent_today_specific_class = ManageStudentSAttendance.objects.filter(
        date=today_date, attendance_status=False, course_name=curent_login_user_its_course).count()

    count_all_student_absent_today = ManageStudentSAttendance.objects.filter(
        date=today_date, attendance_status=False
    ).count()
    get_today_attendance = ManageStudentSAttendance.objects.filter(
        date=today_date
    )
    print('today attendL ', get_today_attendance)
    form3 = ManageStudentSAttendanceForm()
    get_attendance_for_all_student = ManageStudentSAttendance.objects.all(
    ).order_by('-created_at')

    template_name = 'skymarkPages/Dashboard/dashboardPage.html'
    for_data_tables_refresh = 'skymarkPages/Dashboard/datatables.html'
    context = {
        'today_date': today_date,
        'get_today_attendance': get_today_attendance,
        'form3': form3,
        'staff_course_name': staff_course_name,
        'count_all_lessons': count_all_lessons,
        'get_all_lessons': get_all_lessons,
        'count_all_students': count_all_students,
        'count_all_staff': count_all_staff,
        'count_all_courses': count_all_courses,
        'count_all_student_present_today': count_all_student_present_today,
        'count_all_student_absent_today': count_all_student_absent_today,
        'get_staff_permision': get_staff_permision,
        'get_present_student_by_its_course': get_present_student_by_its_course,
        'get_absent_student_by_its_course': get_absent_student_by_its_course,
        'count_all_student_present_today_specific_class': count_all_student_present_today_specific_class,
        'count_all_student_absent_today_specific_class': count_all_student_absent_today_specific_class,
        'get_all_students_by_its_course': get_all_students_by_its_course,
        'get_attendance_for_all_student': get_attendance_for_all_student,
    }
    if request.htmx:
        return render(request, for_data_tables_refresh, context)
    else:
        return render(request, template_name, context)


# manageClassesPage


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
@ login_required(login_url=LOGIN_URL)
def manageClassesPage(request):
    if request.method == 'POST':
        form = ManageClassForm(request.POST)
        class_name = request.POST.get('class_name')
        if form.is_valid():
            instance = form.save(commit=False)
            instance.registered_by = request.user
            instance.save()
            messages.success(request, f'{class_name} added succesfull')
            return redirect('skymarkApp:manageClassesPage')
        else:
            messages.info(
                request, f"Ooops  class not added yet please try again")
            return redirect('skymarkApp:manageClassesPage')
    # Obtain_Staff_permision_
    user = User.objects.get(username=request.user)
    get_staff = ManageStaffDetails.objects.get(username=user)
    try:
        get_staff_permision = ManageAccountPermision.objects.get(
            staff_full_name=get_staff)
    except:
        get_staff_permision = ManageAccountPermision.objects.filter(
            staff_full_name=get_staff)

    count_all_classes = ManageClass.objects.all().count
    get_all_classes = ManageClass.objects.all().order_by('-id')
    template_name = 'skymarkPages/ManageClases/manageClassesPage.html'
    context = {
        'count_all_classes': count_all_classes,
        'get_all_classes': get_all_classes,
        'get_staff_permision': get_staff_permision
    }
    return render(request, template_name, context)

# ManageCoursesPage


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=LOGIN_URL)
def ManageCoursesPage(request):
    if request.method == 'POST':
        form = ManageCoursesForm(request.POST)
        course_name = request.POST.get('course_name')
        if form.is_valid():
            messages.success(request, f'{course_name} added succesfull')
            form.save()
            return redirect('skymarkApp:ManageCoursesPage')
        else:
            messages.info(
                request, f"Ooops  course not added yet please try again")
            return redirect('skymarkApp:ManageCoursesPage')
    # Obtain_Staff_permision_
    user = User.objects.get(username=request.user)
    get_staff = ManageStaffDetails.objects.get(username=user)
    try:
        get_staff_permision = ManageAccountPermision.objects.get(
            staff_full_name=get_staff)
    except:
        get_staff_permision = ManageAccountPermision.objects.filter(
            staff_full_name=get_staff)

    count_all_courses = ManageCourses.objects.all().count
    get_all_courses = ManageCourses.objects.all().order_by('-id')
    get_all_classes = ManageClass.objects.all().order_by('-id')
    form = ManageCoursesForm()
    template_name = 'skymarkPages/ManageCourses/manageCoursesPage.html'
    context = {
        'form': form,
        'get_all_classes': get_all_classes,
        'count_all_courses': count_all_courses,
        'get_all_courses': get_all_courses,
        'get_staff_permision': get_staff_permision
    }
    return render(request, template_name, context)

# manageStudentsDetailsPage


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=LOGIN_URL)
def manageStudentsDetailsPage(request):
    if request.method == 'POST' and request.POST.get('add_student_info'):
        form = ManageStudentDetailsForm(request.POST, request.FILES)
        student_full_name = request.POST.get('student_full_name')
        if form.is_valid():
            messages.success(
                request, f' Student {student_full_name} added succesfull')
            form.save()
            return redirect('skymarkApp:manageStudentsDetailsPage')
        else:
            messages.info(
                request, f"Ooops  Students not added yet please try again")
            return redirect('skymarkApp:manageStudentsDetailsPage')

    # add_student_fees
    if request.method == 'POST' and request.POST.get('add_student_fees'):
        form = ManageStudentFeesForm(request.POST)
        student_id = request.POST.get('student_full_name')
        get_students_full_name = ManageStudentDetails.objects.get(
            id=student_id)
        if form.is_valid():
            form.save()
            messages.success(
                request, f' fees for {get_students_full_name} added succesfull')
            return redirect('skymarkApp:manageStudentsDetailsPage')
        else:
            messages.info(
                request, f"Ooops  fees for {get_students_full_name} not added yet please try again")
            return redirect('skymarkApp:manageStudentsDetailsPage')

    if request.method == 'POST' and request.POST.get('student_is_present'):
        form = ManageStudentSAttendanceForm(request.POST)
        get_students_id = request.POST.get('student_name')
        get_students_full_name = ManageStudentDetails.objects.get(
            id=get_students_id)
        print("===========", get_students_full_name)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.attendance_status = True
            instance.course_name = get_students_full_name.course_name
            instance.save()
            messages.success(
                request, f'Student {get_students_full_name} is present')
            return redirect('skymarkApp:manageStudentsDetailsPage')
        else:
            messages.info(
                request, f"please try again")
            return redirect('skymarkApp:manageStudentsDetailsPage')

    if request.method == 'POST' and request.POST.get('student_is_absent'):
        form = ManageStudentSAttendanceForm(request.POST)
        get_students_id = request.POST.get('student_name')
        get_students_full_name = ManageStudentDetails.objects.get(
            id=get_students_id)
        print("===========", get_students_full_name)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.attendance_status = False
            instance.course_name = get_students_full_name.course_name
            instance.save()
            messages.success(
                request, f'Student {get_students_full_name} is absent')
            return redirect('skymarkApp:manageStudentsDetailsPage')
        else:
            messages.info(
                request, f"please try again")
            return redirect('skymarkApp:manageStudentsDetailsPage')

    # Obtain_Staff_permision_
    user = User.objects.get(username=request.user)
    get_staff = ManageStaffDetails.objects.get(username=user)
    try:
        get_staff_permision = ManageAccountPermision.objects.get(
            staff_full_name=get_staff)
    except:
        get_staff_permision = ManageAccountPermision.objects.filter(
            staff_full_name=get_staff)

    get_attendance_for_all_student = ManageStudentSAttendance.objects.all().order_by('-created_at')
    count_all_students = ManageStudentDetails.objects.all().count
    get_all_students = ManageStudentDetails.objects.all().order_by('-id')
    get_all_fee_from_all_students = ManageStudentFees.objects.all().order_by('-id')
    form = ManageStudentDetailsForm()
    form2 = ManageStudentFeesForm()
    form3 = ManageStudentSAttendanceForm()
    template_name = 'skymarkPages/StudentsDetails/manageStudentsDetailsPage.html'
    context = {
        'form': form,
        'form2': form2,
        'form3': form3,
        'count_all_students': count_all_students,
        'get_all_students': get_all_students,
        'get_all_fee_from_all_students': get_all_fee_from_all_students,
        'get_attendance_for_all_student': get_attendance_for_all_student,
        'get_staff_permision': get_staff_permision,
    }
    return render(request, template_name, context)

# manageStaffDetailsPage


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=LOGIN_URL)
def manageStaffDetailsPage(request):

    if request.method == 'POST' and request.POST.get('add_staff_info'):
        form = ManageStaffDetailsForm(request.POST, request.FILES)
        staff_full_name = request.POST.get('staff_full_name')
        if form.is_valid():
            messages.success(
                request, f'Staff {staff_full_name} added succesfull')
            form.save()
            return redirect('skymarkApp:manageStaffDetailsPage')
        else:

            messages.info(
                request, f"Ooops  staff not added yet please try again")
            return redirect('skymarkApp:manageStaffDetailsPage')

    if request.method == 'POST' and request.POST.get('account_for_staff'):
        form = AccountForStaffForm(request.POST)
        staff_id = request.POST.get('staff_id')
        staff_username = request.POST.get('username')
        get_staff_password = request.POST.get('password1')
        print('===========', staff_id)
        get_staff = ManageStaffDetails.objects.get(
            id=staff_id)
        print('===============', get_staff)
        if form.is_valid():
            form.save()
            get_user = User.objects.get(username=staff_username)
            ManageStaffDetails.objects.filter(
                id=staff_id).update(username=get_user.id)
            messages.success(
                request, f'Account for {get_staff}  created successfull')
            return redirect('skymarkApp:manageStaffDetailsPage')
        else:
            user = authenticate(username=staff_username,
                                password=get_staff_password)
            if user is not None:
                messages.info(
                    request, f"Ooops  {staff_username} Account   arleady Existed ")
            else:
                messages.info(
                    request, f"Ooops Invalid username or password ")
            return redirect('skymarkApp:manageStaffDetailsPage')
    if request.method == 'POST' and request.POST.get('staff_permision'):
        form = ManageAccountPermisionForm(request.POST)
        get_staff_id = request.POST.get('staff_id')
        get_staff_details = ManageStaffDetails.objects.get(id=get_staff_id)
        get_staff_full_name = get_staff_details.staff_full_name
        print('++++++++', get_staff_full_name)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff_full_name = get_staff_details
            instance.save()
            messages.success(
                request, f'Permission for {get_staff_full_name}  created successfull')
            return redirect('skymarkApp:manageStaffDetailsPage')
        return redirect('skymarkApp:manageStaffDetailsPage')

    # Obtain_Staff_permision_
    user = User.objects.get(username=request.user)
    get_staff = ManageStaffDetails.objects.get(username=user)
    try:
        get_staff_permision = ManageAccountPermision.objects.get(
            staff_full_name=get_staff)
    except:
        get_staff_permision = ManageAccountPermision.objects.filter(
            staff_full_name=get_staff)

    count_all_staff = ManageStaffDetails.objects.all().count
    get_all_staff = ManageStaffDetails.objects.all().order_by('-id')
    form = ManageStaffDetailsForm()
    form2 = AccountForStaffForm()
    form3 = ManageAccountPermisionForm()
    template_name = 'skymarkPages/StaffDetails/manageStaffDetailsPage.html'
    context = {
        'form': form,
        'form2': form2,
        'form3': form3,
        'count_all_staff': count_all_staff,
        'get_all_staff': get_all_staff,
        'get_staff_permision': get_staff_permision,
    }
    return render(request, template_name, context)

# manageLessonToughtAtCollegePage


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=LOGIN_URL)
def manageLessonToughtAtCollegePage(request):
    if request.method == 'POST' and request.POST.get('lesson_tought'):
        form = ManageLessonToughtAtCollegeForm(request.POST)
        lesson = request.POST.get('topic_covered')
        if form.is_valid():
            messages.success(
                request, f' Your lesson {lesson}  submited successfull')
            instance = form.save(commit=False)
            instance.submited_by = request.user
            instance.save()
            return redirect('skymarkApp:manageLessonToughtAtCollegePage')
        else:
            messages.info(
                request, f"Ooops  Your lesson not  submited yet please try again")
            return redirect('skymarkApp:manageStaffDetailsPage')
    # Obtain_Staff_permision_
    user = User.objects.get(username=request.user)
    get_staff = ManageStaffDetails.objects.get(username=user)
    try:
        get_staff_permision = ManageAccountPermision.objects.get(
            staff_full_name=get_staff)
    except:
        get_staff_permision = ManageAccountPermision.objects.filter(
            staff_full_name=get_staff)

    get_user = User.objects.get(username=request.user)
    count_user_lesson = ManageLessonToughtAtCollege.objects.filter(
        submited_by=get_user).count()

    get_user_lessons = ManageLessonToughtAtCollege.objects.filter(
        submited_by=get_user)
    print('+++++++++++', count_user_lesson)
    form = ManageLessonToughtAtCollegeForm()
    template_name = 'skymarkPages/LessonToughtAtCollege/manageLessonToughtAtCollegePage.html'
    context = {
        'form': form,
        'count_user_lesson': count_user_lesson,
        'get_user_lessons': get_user_lessons,
        'get_staff_permision': get_staff_permision,
    }
    return render(request, template_name, context)

# logOutUser


def logOutUser(request):
    logout(request)
    return redirect('skymarkApp:loginPage')
