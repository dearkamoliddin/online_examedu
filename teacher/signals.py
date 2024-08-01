import os
import json
from conf.settings import BASE_DIR
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from teacher.models import TeacherModel


@receiver(post_save, sender=TeacherModel)
def teacher_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.full_name} is created')
        print(kwargs)
    else:
        print('Teacher is Updated')


post_save.connect(teacher_save, sender=TeacherModel)


@receiver(pre_delete, sender=TeacherModel)
def teacher_delete(sender, instance, **kwargs):
    teacher_data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'speciality': instance.speciality,
        'bio': instance.bio,
    }
    file_path = os.path.join(BASE_DIR, f'teacher/deleted_teachers/{instance.full_name}.json')
    with open(file_path, mode='w') as file_json:
        json.dump(teacher_data, file_json, indent=4)

    print(f'{instance.full_name} is deleted')
