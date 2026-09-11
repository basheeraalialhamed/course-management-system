from django.shortcuts import get_object_or_404 ,redirect,render
from decimal import Decimal,InvalidOperation
from ..models import Course , Enrollment
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q , Count
from django.contrib.auth.models import User


def course_list(request):
    courses = Course.objects.all()

    return render(request, "courses/course_list.html", {
        "courses": courses
    })

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    return render(request, "courses/course_detail.html", {
        "course": course
    })


def courses_manager_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if not hasattr(request.user, "profile"):
            raise PermissionDenied

        if request.user.profile.role != "courses_manager":
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper
@courses_manager_required
def course_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        price_text = request.POST.get("price", "").strip()
        image = request.FILES.get("image")

        if not title or not description or not price_text:
            return render(
                request,
                "courses/course_create.html",
                {
                    "error": "يرجى تعبئة جميع الحقول المطلوبة."
                }
            )

        if not image:
            return render(
                request,
                "courses/course_create.html",
                {
                    "error": "يرجى اختيار صورة للدورة."
                }
            )

        if Course.objects.filter(title__iexact=title).exists():
            return render(
                request,
                "courses/course_create.html",
                {
                    "error": "هذه الدورة موجودة مسبقًا، يرجى اختيار عنوان آخر."
                }
            )

        try:
            price = Decimal(price_text)

            if price < 0:
                return render(
                    request,
                    "courses/course_create.html",
                    {
                        "error": "لا يمكن أن يكون سعر الدورة سالبًا."
                    }
                )

            course = Course.objects.create(
                title=title,
                description=description,
                price=price,
                image=image
            )

        except InvalidOperation:
            return render(
                request,
                "courses/course_create.html",
                {
                    "error": "يرجى إدخال سعر صحيح."
                }
            )

        except Exception:
            return render(
                request,
                "courses/course_create.html",
                {
                    "error": (
                        "حدث خطأ غير متوقع أثناء إضافة الدورة، "
                        "يرجى المحاولة مرة أخرى."
                    )
                }
            )

        return redirect(
            "course_detail",
            pk=course.pk
        )
    

    return render(
        request,
        "courses/course_create.html"
    )
    
@courses_manager_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.title = request.POST["title"]
        course.description = request.POST["description"]
        course.price = request.POST["price"]

        if request.FILES.get("image"):
            course.image = request.FILES.get("image")

        course.save()

        return redirect("course_detail", pk=course.pk)

    return render(request, "courses/course_update.html", {
        "course": course
    })
@courses_manager_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()

        return redirect("course_list")

    return render(request, "courses/course_delete.html", {
        "course": course
    })



@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.user.profile.role != "student":
        raise PermissionDenied

    existing_enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    if existing_enrollment:
        messages.warning(
            request,
            "لقد أرسلت طلب تسجيل لهذه الدورة مسبقًا."
        )
        return redirect("student_dashboard")

    Enrollment.objects.create(
        student=request.user,
        course=course,
        status="pending"
    )

    messages.success(
        request,
        "تم إرسال طلب التسجيل بنجاح، وبانتظار موافقة مدير الدورات."
    )

    return redirect("student_dashboard")

@login_required
def student_dashboard(request):

    if request.user.profile.role != "student":
        raise PermissionDenied

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course")

    return render(
        request,
        "courses/student_dashboard.html",
        {
            "enrollments": enrollments
        }
    )
@login_required
def courses_manager_dashboard(request):

    if request.user.profile.role != "courses_manager":
        raise PermissionDenied

    courses = Course.objects.all()

    enrollments = Enrollment.objects.select_related(
        "student",
        "course"
    ).order_by("-enrolled_at")

    # الإحصائيات

    total_courses = courses.count()

    total_students = User.objects.filter(
        profile__role="student"
    ).count()

    total_enrollments = enrollments.count()

    pending_enrollments = enrollments.filter(
        status="pending"
    ).count()

    approved_enrollments = enrollments.filter(
        status="approved"
    ).count()

    rejected_enrollments = enrollments.filter(
        status="rejected"
    ).count()

    return render(
        request,
        "courses/courses_manager_dashboard.html",
        {
            "courses": courses,
            "enrollments": enrollments,

            "total_courses": total_courses,
            "total_students": total_students,
            "total_enrollments": total_enrollments,
            "pending_enrollments": pending_enrollments,
            "approved_enrollments": approved_enrollments,
            "rejected_enrollments": rejected_enrollments,
        }
    )
@courses_manager_required
def enrollment_management(request):

    search = request.GET.get("search", "").strip()
    course_id = request.GET.get("course", "").strip()

    enrollments = Enrollment.objects.select_related(
        "student",
        "course"
    ).order_by("-enrolled_at")

    if search:
        enrollments = enrollments.filter(
            Q(student__username__icontains=search)
            | Q(course__title__icontains=search)
        )

    if course_id:
        enrollments = enrollments.filter(
            course_id=course_id
        )

    courses = Course.objects.all().order_by("title")

    # الدورات المطابقة لاسم البحث
    searched_courses = Course.objects.filter(
        title__icontains=search
    ).annotate(
        enrollment_count=Count("enrollments")
    ).prefetch_related(
        "enrollments__student"
    ) if search else Course.objects.none()

    return render(
        request,
        "courses/enrollment_management.html",
        {
            "enrollments": enrollments,
            "courses": courses,
            "search": search,
            "selected_course": course_id,
            "searched_courses": searched_courses,
        }
    )

@courses_manager_required
def student_management(request):

    search = request.GET.get("search", "").strip()

    students = User.objects.filter(
        profile__role="student"
    ).prefetch_related(
        "enrollments__course"
    ).order_by("username")

    if search:
        students = students.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
        )

    return render(
        request,
        "courses/student_management.html",
        {
            "students": students,
            "search": search,
        }
    )
@courses_manager_required
def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.method == "POST":
        enrollment.delete()
        return redirect("enrollment_management")

    return render(
        request,
        "courses/enrollment_delete.html",
        {"enrollment": enrollment}
    )

@courses_manager_required
def enrollment_approve(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.method == "POST":
        enrollment.status = "approved"
        enrollment.save()

    return redirect("enrollment_management")


@courses_manager_required
def enrollment_reject(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.method == "POST":
        enrollment.status = "rejected"
        enrollment.save()

    return redirect("enrollment_management")