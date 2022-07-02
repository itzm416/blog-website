from django.db import models
from django.utils.html import format_html
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from autoslug import AutoSlugField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    image = models.ImageField(upload_to='category/')
    add_date = models.DateTimeField(auto_now_add=True,null=True)

    def image_tag(self):
        return format_html(f'<img src="/media/{self.image}" style="width:40px;height:40px;border-radius:50%;"  />')
    
    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    post_id = models.AutoField(primary_key=True)
    blogviews=models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post/')
    add_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-add_date',]

    def image_tag(self):
        return format_html(f'<img src="/media/{self.image}" style="width:40px;height:40px;border-radius:50%;"  />')

    def __str__(self):
        return self.title