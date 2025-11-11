from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.exceptions import PermissionDenied
# Create your models here.


class User(AbstractUser):
    ROLES = (
        ('LIBRARIAN', 'LIBRARIAN'),
        ('STUDENT', 'STUDENT'),)

    role = models.CharField(max_length=20, choices=ROLES, default='STUDENT')

    def save(self, *args, **kwargs):
        if self.role == 'LIBRARIAN':
            self.is_staff = True
            self.is_superuser = True
        super(User, self).save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    available_copies = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100)
    def __str__(self):
        return self.title
    
    def get_url(self):
        return reverse('book_detail', args=[self.slug])

from datetime import timedelta , date
class BookIssue(models.Model):
    STATUS = (
        ('REQUESTED', 'REQUESTED'),
        ('RETURNED', 'RETURNED'),
        ('APPROVED', 'APPROVED'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    renual_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='REQUESTED')

    def __str__(self):
        return f"{self.book} - {self.user}"
    
    def get_url(self):
        return reverse('update_status', args=[self.id])
    def save(self, *args, **kwargs):        
        if self.pk:
            old_status = BookIssue.objects.get(pk=self.pk).status
            if old_status != self.status:
                if self.status == 'RETURNED':
                    self.return_date = date.today()
                    self.book.available_copies += 1
                    
                elif self.status == 'APPROVED':
                    self.issue_date = date.today()
                    self.renual_date = date.today() + timedelta(days=15)
                    self.book.available_copies -= 1
                self.book.save()
        else:
            if self.status == 'APPROVED':
                self.issue_date = date.today()
                self.renual_date = date.today() + timedelta(days=15)
                self.book.available_copies -= 1
                self.book.save()
                   
        super(BookIssue, self).save(*args, **kwargs)
                    
                            
                
            