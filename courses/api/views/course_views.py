
from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from ..serializers import CourseSerializer
from ...models import Course


class CourseListAPIView(generics.ListAPIView):

    serializer_class = CourseSerializer

    def get_queryset(self):

        try:
            search = self.request.query_params.get(
                "search",
                ""
            ).strip()

            courses = Course.objects.all()

            if search:
                courses = courses.filter(
                    Q(title__icontains=search)
                    | Q(description__icontains=search)
                )

            return courses

        except Exception:
            return Course.objects.none()


class CourseDetailAPIView(generics.RetrieveAPIView):

    queryset = Course.objects.all()

    serializer_class = CourseSerializer


class CourseCreateAPIView(generics.CreateAPIView):

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        try:
            if self.request.user.profile.role != "courses_manager":
                raise PermissionDenied(
                    "فقط مدير الدورات يستطيع إنشاء دورة."
                )

            serializer.save()

        except PermissionDenied:
            raise

        except Exception:
            raise PermissionDenied(
                "حدث خطأ أثناء إنشاء الدورة."
            )


class CourseUpdateAPIView(generics.UpdateAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):

        try:
            if self.request.user.profile.role != "courses_manager":
                raise PermissionDenied(
                    "فقط مدير الدورات يستطيع تعديل الدورة."
                )

            serializer.save()

        except PermissionDenied:
            raise

        except Exception:
            raise PermissionDenied(
                "حدث خطأ أثناء تعديل الدورة."
            )


class CourseDeleteAPIView(generics.DestroyAPIView):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):

        try:
            if self.request.user.profile.role != "courses_manager":
                raise PermissionDenied(
                    "فقط مدير الدورات يستطيع حذف الدورة."
                )

            instance.delete()

        except PermissionDenied:
            raise

        except Exception:
            raise PermissionDenied(
                "حدث خطأ أثناء حذف الدورة."
            )


