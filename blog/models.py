from django.db import models


class AuthorModel(models.Model):
    full_name = models.CharField(max_length=100)
    education = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

    def str(self):
        return self.full_name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class BlogModel(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE)

    def str(self):
        return self.title

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'



