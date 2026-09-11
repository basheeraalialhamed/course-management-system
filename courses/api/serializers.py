from rest_framework import serializers

from ..models import Course, Enrollment


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "price",
            "image",
            "created_at",
        ]


class EnrollmentSerializer(serializers.ModelSerializer):

    student = serializers.CharField(
        source="student.username",
        read_only=True
    )

    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )

    course_name = serializers.CharField(
        source="course.title",
        read_only=True
    )

    def validate_course(self, value):
        request = self.context.get("request")

        try:
            if request and request.user.is_authenticated:

                exists = Enrollment.objects.filter(
                    student=request.user,
                    course=value
                ).exists()

                if exists:
                    raise serializers.ValidationError(
                        "لقد أرسلت طلب تسجيل لهذه الدورة مسبقًا."
                    )

        except serializers.ValidationError:
            raise

        except Exception:
            raise serializers.ValidationError(
                "حدث خطأ أثناء التحقق من طلب التسجيل."
            )

        return value

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "course",
            "course_name",
            "status",
            "enrolled_at",
        ]
        read_only_fields = [
            "id",
            "student",
            "course_name",
            "status",
            "enrolled_at",
        ]