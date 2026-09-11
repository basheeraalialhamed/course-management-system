from django.db import IntegrityError

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from ...models import Enrollment
from ..serializers import EnrollmentSerializer


class EnrollmentListAPIView(generics.ListAPIView):

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.profile.role == "courses_manager":
            return Enrollment.objects.all()

        return Enrollment.objects.filter(
            student=self.request.user
        )


class MyEnrollmentsAPIView(generics.ListAPIView):

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Enrollment.objects.filter(
            student=self.request.user
        )


class EnrollmentCreateAPIView(generics.CreateAPIView):

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        if self.request.user.profile.role != "student":
            raise PermissionDenied(
                "فقط الطالب يستطيع إرسال طلب تسجيل."
            )

        try:
            serializer.save(
                student=self.request.user,
                status="pending"
            )

        except IntegrityError:
            raise ValidationError({
                "course": [
                    "لقد أرسلت طلب تسجيل لهذه الدورة مسبقًا."
                ]
            })


class EnrollmentApproveAPIView(generics.UpdateAPIView):

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):

        try:
            if request.user.profile.role != "courses_manager":
                raise PermissionDenied(
                    "فقط مدير الدورات يستطيع الموافقة على الطلبات."
                )

            enrollment = self.get_object()

            if enrollment.status != "pending":
                raise ValidationError({
                    "status": "هذا الطلب تمت معالجته مسبقًا."
                })

            enrollment.status = "approved"
            enrollment.save()

            serializer = self.get_serializer(enrollment)

            return Response(serializer.data)

        except PermissionDenied:
            raise

        except ValidationError:
            raise

        except Exception:
            return Response(
                {
                    "error": "حدث خطأ غير متوقع أثناء الموافقة على الطلب."
                },
                status=500
            )


class EnrollmentRejectAPIView(generics.UpdateAPIView):

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):

        try:
            if request.user.profile.role != "courses_manager":
                raise PermissionDenied(
                    "فقط مدير الدورات يستطيع رفض الطلبات."
                )

            enrollment = self.get_object()

            if enrollment.status != "pending":
                raise ValidationError({
                    "status": "هذا الطلب تمت معالجته مسبقًا."
                })

            enrollment.status = "rejected"
            enrollment.save()

            serializer = self.get_serializer(enrollment)

            return Response(serializer.data)

        except PermissionDenied:
            raise

        except ValidationError:
            raise

        except Exception:
            return Response(
                {
                    "error": "حدث خطأ غير متوقع أثناء رفض الطلب."
                },
                status=500
            )