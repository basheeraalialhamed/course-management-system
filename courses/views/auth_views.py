from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout
from ..models import Profile

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        if not username:
            return render(
                request,
                "courses/register.html",
                {"error": "يرجى إدخال اسم المستخدم."}
            )

        if password != password2:
            return render(
                request,
                "courses/register.html",
                {"error": "كلمتا المرور غير متطابقتين."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "courses/register.html",
                {"error": "اسم المستخدم موجود بالفعل."}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            role="student"
        )

        login(request, user)

        return redirect("course_list")

    return render(request, "courses/register.html")





def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("course_list")

        return render(
            request,
            "courses/login.html",
            {
                "error": "اسم المستخدم أو كلمة المرور غير صحيحة."
            }
        )

    return render(
        request,
        "courses/login.html"
    )


def user_logout(request):

    if request.method == "POST":
        logout(request)

        return redirect("course_list")

    return render(
        request,
        "courses/logout.html"
    )