from datetime import datetime
import os
from itertools import product
from django.db import models
import uuid
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class ManageClass(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    class_name = models.CharField(max_length=100)
    registered_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # always change when object is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Skymark VTC classes'

    def __str__(self):
        return str(self.class_name)


class ManageCourses(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    course_name = models.CharField(max_length=100, null=True, blank=True)
    course_content = RichTextField()
    course_duration = models.CharField(max_length=100, null=True, blank=True)
    course_cost = models.CharField(max_length=100, null=True, blank=True)
    class_name = models.ForeignKey(
        ManageClass, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # always change when object is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Skymark VTC courses Offered'

    def __str__(self):
        return str(self.course_name)


class ManageStudentDetails(models.Model):
    GENDER = (
        ('', 'select gender'),
        ('male', 'male'),
        ('female', 'female'),
    )
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    student_image = models.ImageField(upload_to='media/')
    student_full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=100, null=True, blank=True, choices=GENDER)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=100, null=True, blank=True)
    parent_name = models.CharField(max_length=100, null=True, blank=True)
    parent_phone_number = models.CharField(
        max_length=100, null=True, blank=True)
    course_name = models.ForeignKey(
        ManageCourses, on_delete=models.SET_NULL, null=True, blank=True)
    today_attendence = models.BooleanField(default=False)
    admission_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # always change when object is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Students Lists at Skymark VTC'

    def __str__(self):
        return str(self.student_full_name)


class ManageStudentFees(models.Model):
    student_full_name = models.ForeignKey(
        ManageStudentDetails, on_delete=models.SET_NULL, null=True, blank=True)
    amount_paid = models.PositiveIntegerField()
    date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # always change when object is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Students Fees Lists at Skymark VTC'

    def __str__(self):
        return str(self.student_full_name)


class ManageStudentSAttendance(models.Model):
    student_name = models.ForeignKey(
        ManageStudentDetails, on_delete=models.SET_NULL, null=True, blank=True)
    course_name = models.ForeignKey(
        ManageCourses, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    attendance_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # always change when object is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Students attendance Lists at Skymark VTC'

    def __str__(self):
        return str(self.student_name)


class ManageStaffDetails(models.Model):
    GENDER = (
        ('', 'select gender'),
        ('male', 'male'),
        ('female', 'female'),
    )
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    staff_image = models.ImageField(upload_to='media/')
    staff_full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        max_length=100, null=True, blank=True,  choices=GENDER)
    dob = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        max_length=100, null=True, blank=True)
    class_name = models.ForeignKey(
        ManageCourses, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.CharField(max_length=100, null=True, blank=True)
    username = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # always change when object is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Staff Lists at Skymark VTC'

    def __str__(self):
        return str(self.staff_full_name)


class ManageLessonToughtAtCollege(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    date = models.DateField(blank=True, null=True)
    topic_covered = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=1000, null=True, blank=True)
    submited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # always change when object is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Daily Lesson Tought'

    def __str__(self):
        return str(self.submited_by)


class ManageAccountPermision(models.Model):
    staff_full_name = models.ForeignKey(
        ManageStaffDetails, on_delete=models.SET_NULL, null=True, blank=True)
    staff_can_add_or_edit_or_delete_classes = models.BooleanField(
        default=False)
    staff_can_add_or_edit_or_delete_courses = models.BooleanField(
        default=False)
    staff_can_add_or_edit_or_delete_student_details = models.BooleanField(
        default=False)

    staff_can_add_or_edit_or_delete_staff_details = models.BooleanField(
        default=False)

    staff_can_add_or_edit_or_delete_lessons = models.BooleanField(
        default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # always change when object is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Staff permision'

    def __str__(self):
        return str(self.staff_full_name)
