from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from django import forms
from django.conf import settings


class XYZ_DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        # kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class ManageClassForm(ModelForm):
    class Meta:
        model = ManageClass
        fields = '__all__'
        exclude = [
            'registered_by',
            'created_at',
            'updated_at'
        ]


class ManageCoursesForm(ModelForm):
    class Meta:
        model = ManageCourses
        fields = '__all__'
        exclude = [
            'created_at',
            'updated_at'
        ]


class ManageStudentDetailsForm(ModelForm):

    class Meta:
        model = ManageStudentDetails
        fields = '__all__'
        exclude = [
            'today_attendence',
            'created_at',
            'updated_at'
        ]
        widgets = {
            'birth_date': XYZ_DateInput(format=["%Y-%m-%d"],),
            'admission_date': XYZ_DateInput(format=["%Y-%m-%d"],),

        }


class ManageStudentFeesForm(ModelForm):
    class Meta:
        model = ManageStudentFees
        fields = '__all__'
        exclude = [
            'created_at',
            'updated_at'
        ]

        widgets = {
            'date': XYZ_DateInput(format=["%Y-%m-%d"],),

        }


class ManageStudentSAttendanceForm(ModelForm):
    class Meta:
        model = ManageStudentSAttendance
        fields = '__all__'
        exclude = [
            'course_name',
            'created_at',
            'updated_at'
        ]

        widgets = {
            'date': XYZ_DateInput(format=["%Y-%m-%d"],),

        }


class ManageStaffDetailsForm(ModelForm):
    class Meta:
        model = ManageStaffDetails
        fields = '__all__'
        exclude = [
            'username',
            'created_at',
            'updated_at'
        ]

        widgets = {
            'dob': XYZ_DateInput(format=["%Y-%m-%d"],),
            'admission_date': XYZ_DateInput(format=["%Y-%m-%d"],),

        }


class ManageLessonToughtAtCollegeForm(ModelForm):
    class Meta:
        model = ManageLessonToughtAtCollege
        fields = '__all__'
        exclude = [
            'created_at',
            'updated_at'
        ]
        widgets = {
            'date': XYZ_DateInput(format=["%Y-%m-%d"],),

        }


class AccountForStaffForm(UserCreationForm):
    staff_id = forms.CharField(max_length=2000)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        exclude = [
            'created_at',
            'updated_at'
        ]


class ManageAccountPermisionForm(ModelForm):
    class Meta:
        model = ManageAccountPermision
        fields = '__all__'
        exclude = [
            'created_at',
            'updated_at'
        ]
