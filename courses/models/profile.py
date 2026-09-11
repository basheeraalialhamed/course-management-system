from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):

    ROLE_CHOICES = (
        ("student", "طالب"),
        ("courses_manager", "مدير الدورات"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="المستخدم"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name="نوع المستخدم"
    )

    def str(self):
        return self.user.username