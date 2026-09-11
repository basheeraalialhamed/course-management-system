
from django.urls import path

from .views import (
    course_list,
    course_detail,
    course_create,
    course_update,
    course_delete,
    register,
    user_login,
    user_logout,
    enroll_course,
    enrollment_approve,
    enrollment_reject,
    student_dashboard,
    courses_manager_dashboard,
    enrollment_management,
    enrollment_delete,
    student_management,

)
urlpatterns = [

    
    path("", course_list, name="course_list"),

    path(
        "courses/<int:pk>/",
        course_detail,
        name="course_detail"
    ),

    path(
        "courses/create/",
        course_create,
        name="course_create"
    ),

    path(
        "courses/<int:pk>/update/",
        course_update,
        name="course_update"
    ),

    path(
        "courses/<int:pk>/delete/",
        course_delete,
        name="course_delete"
    ),
    
    path(
        "register/",
        register,
        name="register"
    ),

    path(
        "login/",
        user_login,
        name="login"
    ),

    path(
        "logout/",
        user_logout,
        name="logout"
    ),
    path(
    "logout/",
    user_logout,
    name="logout"
),
path("courses/<int:pk>/enroll/", enroll_course, name="enroll_course"),
path(
    "student/dashboard/",
    student_dashboard,
    name="student_dashboard"
),
path(
    "manager/dashboard/",
    courses_manager_dashboard,
    name="courses_manager_dashboard"
),
path(
    "manager/enrollments/",
    enrollment_management,
    name="enrollment_management"
),
path(
    "manager/enrollments/<int:pk>/delete/",
    enrollment_delete,
    name="enrollment_delete"
),
path(
    "manager/enrollments/<int:pk>/approve/",
    enrollment_approve,
    name="enrollment_approve"
),

path(
    "manager/enrollments/<int:pk>/reject/",
    enrollment_reject,
    name="enrollment_reject"
),
path(
    "manager/students/",
    student_management,
    name="student_management"
),
]

