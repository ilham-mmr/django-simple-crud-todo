from django.db import models


# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=100)


class Todo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_done = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        Tag, null=True, blank=True, related_name='todos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
