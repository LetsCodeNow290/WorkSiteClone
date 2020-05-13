from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    TITLE_CHOICES = (('EMS 901', 'EMS 901'), ('EMS 902', 'EMS 902'))
    title = models.CharField(max_length=100, choices=TITLE_CHOICES)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('blog_detail', kwargs={'pk': self.pk})