from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000)]
    )
    stock = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

class CustomUser(AbstractUser):
    REGULAR = 'regular'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (REGULAR, 'Regular User'),
        (ADMIN, 'Administrator'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=REGULAR)
    borrowed_books = models.ManyToManyField(Book, through='BorrowRecord', related_name='borrowers')
        
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    
    def is_admin(self):
        return self.role == self.ADMIN
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class BorrowRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-borrow_date']
    
    def __str__(self):
        status = "returned" if self.returned else "borrowed"
        return f"{self.user.username} {status} {self.book.title}"