from django.db import models


class TeacherModel(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    speciality = models.CharField(max_length=100)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to='media/teachers/', null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


