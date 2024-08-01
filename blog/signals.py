
import os
import json
from conf.settings import BASE_DIR
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from blog.models import AuthorModel, BlogModel


@receiver(post_save, sender=BlogModel)
def blog_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.name} is created')
        print(kwargs)
    else:
        print('Blog is Updated')


post_save.connect(blog_save, sender=BlogModel)


@receiver(post_save, sender=AuthorModel)
def author_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.full_name} is created')
        print(kwargs)
    else:
        print('Author is Updated')


post_save.connect(author_save, sender=AuthorModel)


@receiver(pre_delete, sender=BlogModel)
def blog_delete(sender, instance, **kwargs):
    blog_data = {
        'id': instance.id,
        'title': instance.title,
        'content': instance.content,
        'date': instance.pub_date,
        'author': instance.author,
    }
    file_path = os.path.join(BASE_DIR, f'blog/deleted_blogs/{instance.title}.json')
    with open(file_path, mode='w') as file_json:
        json.dump(blog_data, file_json, indent=4)

    print(f'{instance.title} is deleted')


@receiver(pre_delete, sender=AuthorModel)
def author_delete(sender, instance, **kwargs):
    author_data = {
        'id': instance.id,
        'full name': instance.full_name,
        'education': instance.education,
    }
    file_path = os.path.join(BASE_DIR, f'blog/deleted_authors/{instance.full_name}.json')
    with open(file_path, mode='w') as file_json:
        json.dump(author_data, file_json, indent=4)

    print(f'{instance.full_name} is deleted')
