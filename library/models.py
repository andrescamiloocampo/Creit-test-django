from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Modelo que representa un libro en la biblioteca
class Book(models.Model):
    """
    Modelo para almacenar información de libros.
    Campos:
        - title: Título del libro
        - author: Autor del libro
        - publication_year: Año de publicación
        - stock: Cantidad de ejemplares disponibles
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000)]
    )
    stock = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        """Representación legible del libro."""
        return f"{self.title} by {self.author} ({self.publication_year})"

# Modelo de usuario personalizado con roles
class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser.
    Campos adicionales:
        - email: Correo electrónico único
        - role: Rol del usuario (regular o admin)
        - borrowed_books: Libros prestados (relación ManyToMany a través de BorrowRecord)
    """
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
        """Devuelve True si el usuario es administrador."""
        return self.role == self.ADMIN
    
    def __str__(self):
        """Representación legible del usuario."""
        return f"{self.username} ({self.get_role_display()})"

# Modelo que representa el registro de préstamos de libros
class BorrowRecord(models.Model):
    """
    Modelo intermedio para registrar los préstamos de libros.
    Campos:
        - user: Usuario que realiza el préstamo
        - book: Libro prestado
        - borrow_date: Fecha de préstamo
        - return_date: Fecha de devolución
        - returned: Estado del préstamo
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-borrow_date']
    
    def __str__(self):
        """Representación legible del registro de préstamo."""
        status = "returned" if self.returned else "borrowed"
        return f"{self.user.username} {status} {self.book.title}"