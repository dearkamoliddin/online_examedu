import os
import json
from conf.settings import BASE_DIR
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from course.models import CourseModel, CommentModel, CategoryModel


@receiver(post_save, sender=CourseModel)
def course_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.title} is created')
        print(kwargs)
    else:
        print('Course is Updated')


post_save.connect(course_save, sender=CourseModel)


@receiver(post_save, sender=CategoryModel)
def category_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.name} is created')
        print(kwargs)
    else:
        print('Category is Updated')


post_save.connect(category_save, sender=CategoryModel)


@receiver(post_save, sender=CommentModel)
def comment_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.name} is created')
        print(kwargs)
    else:
        print('Comment is Updated')


post_save.connect(comment_save, sender=CommentModel)


@receiver(pre_delete, sender=CourseModel)
def course_delete(sender, instance, **kwargs):
    course_data = {
        'id': instance.id,
        'title': instance.title,
        'description': instance.description,
        'price': instance.price,
        'teachers': instance.teachers,
    }
    file_path = os.path.join(BASE_DIR, f'course/deleted_courses/{instance.title}.json')
    with open(file_path, mode='w') as file_json:
        json.dump(course_data, file_json, indent=4)

    print(f'{instance.title} is deleted')


@receiver(pre_delete, sender=CategoryModel)
def category_delete(sender, instance, **kwargs):
    category_data = {
        'id': instance.id,
        'name': instance.name,
    }
    file_path = os.path.join(BASE_DIR, f'course/deleted_categories/{instance.name}.json')
    with open(file_path, mode='w') as file_json:
        json.dump(category_data, file_json, indent=4)

    print(f'{instance.name} is deleted')


@receiver(pre_delete, sender=CommentModel)
def comment_delete(sender, instance, **kwargs):
    comment_data = {
        'id': instance.id,
        'name': instance.name,
        'email': instance.email,
        'rating': instance.rating,
        'course': instance.course,
        'blog': instance.blog,
        'author': instance.author,
    }
    file_path = os.path.join(BASE_DIR, f'course/deleted_comments/{instance.name}.json')
    with open(file_path, mode='w') as file_json:
        json.dump(comment_data, file_json, indent=4)

    print(f'{instance.name} is deleted')
