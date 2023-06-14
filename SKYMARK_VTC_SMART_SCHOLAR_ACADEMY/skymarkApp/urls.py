from django.urls import path, include
from . import views

app_name = 'skymarkApp'

urlpatterns = [
    path('', views.loginPage, name="loginPage"),
    path('dashboard-page', views.dashboardPage, name="dashboardPage"),
    path('manage-classes', views.manageClassesPage, name="manageClassesPage"),
    path('manage-courses', views.ManageCoursesPage, name="ManageCoursesPage"),
    path('manage-students', views.manageStudentsDetailsPage,
         name="manageStudentsDetailsPage"),
    path('manage-staff', views.manageStaffDetailsPage,
         name="manageStaffDetailsPage"),
    path('manage-lesson', views.manageLessonToughtAtCollegePage,
         name="manageLessonToughtAtCollegePage"),
    path('logout-user', views.logOutUser, name="logOutUser"),

]
