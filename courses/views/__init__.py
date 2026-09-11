from .course_views import (
course_list,
course_detail,
course_create,
course_update,
course_delete,
enroll_course,
student_dashboard,
courses_manager_dashboard,
enrollment_management,
enrollment_delete,
enrollment_approve,
enrollment_reject,
student_management,
)

from .auth_views import (
    register,user_login,
    user_logout )