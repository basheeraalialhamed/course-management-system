from django.urls import path

from .views.course_views import (
    CourseListAPIView,
    CourseDetailAPIView,
    CourseCreateAPIView,
    CourseDeleteAPIView,
    CourseUpdateAPIView,
)

from .views.enrollment_views import (
    EnrollmentListAPIView,
    MyEnrollmentsAPIView,
    EnrollmentCreateAPIView,
    EnrollmentApproveAPIView,
    EnrollmentRejectAPIView,
    EnrollmentApproveAPIView,
    EnrollmentListAPIView,
    
)


urlpatterns = [
    path(
        "courses/",
        CourseListAPIView.as_view(),
        name="api_course_list"
    ),

    path(
        "courses/<int:pk>/",
        CourseDetailAPIView.as_view(),
        name="api_course_detail"
    ),

    path(
        "enrollments/",
        EnrollmentListAPIView.as_view(),
        name="api_enrollment_list"
    ),
    path(
    "my-enrollments/",
    MyEnrollmentsAPIView.as_view(),
    name="api_my_enrollments"
),

path(
    "enrollments/create/",
    EnrollmentCreateAPIView.as_view(),
    name="api_enrollment_create"
),

path(
    "enrollments/<int:pk>/approve/",
    EnrollmentApproveAPIView.as_view(),
    name="api_enrollment_approve"
),

path(
    "enrollments/<int:pk>/reject/",
    EnrollmentRejectAPIView.as_view(),
    name="api_enrollment_reject"
),
path(
    "courses/create/",
    CourseCreateAPIView.as_view(),
    name="api_course_create"
),

path(
    "courses/<int:pk>/update/",
    CourseUpdateAPIView.as_view(),
    name="api_course_update"
),

path(
    "courses/<int:pk>/delete/",
    CourseDeleteAPIView.as_view(),
    name="api_course_delete"
),
]