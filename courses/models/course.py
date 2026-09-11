from django.db import models
class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="اسم الدورة"
    )

    description = models.TextField(
        verbose_name="وصف الدورة"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="سعر الدورة"
    )

    image = models.ImageField(
        upload_to="courses/",
        blank=False,
        null=True,
        verbose_name="صورة الدورة"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )

    def str(self):
        return self.title
