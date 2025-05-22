from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from library.models import Book
import random

class Command(BaseCommand):
    help = 'Seed the database with initial admin user and sample books'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Crear usuario admin si no existe
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@library.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        regular_user, regular_created = User.objects.get_or_create(
            username='user',
            defaults={
                'email': 'user@library.com',
                'role': 'regular',
                'is_staff': False,
                'is_superuser': False
            }
        )
                
        if created:
            admin_user.set_password('admin123')
            admin_user.save()            
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        if regular_created:
            regular_user.set_password('user1234')
            regular_user.save()
            self.stdout.write(self.style.SUCCESS('Regular user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Regular user already exists'))    

        # Borrar todos los libros existentes
        Book.objects.all().delete()
        self.stdout.write(self.style.WARNING('All existing books deleted'))

        # Datos de libros para insertar
        books_data = [
            {
                'title': 'Cien años de soledad',
                'author': 'Gabriel García Márquez',
                'publication_year': 1967,
                'stock': random.randint(1, 10)
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'publication_year': 1949,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'Don Quijote de la Mancha',
                'author': 'Miguel de Cervantes',
                'publication_year': 1605,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'Orgullo y prejuicio',
                'author': 'Jane Austen',
                'publication_year': 1813,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'El Principito',
                'author': 'Antoine de Saint-Exupéry',
                'publication_year': 1943,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'El Aleph',
                'author': 'Jorge Luis Borges',
                'publication_year': 1945,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'La sombra del viento',
                'author': 'Carlos Ruiz Zafón',
                'publication_year': 2001,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'Crónica de una muerte anunciada',
                'author': 'Gabriel García Márquez',
                'publication_year': 1981,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'Rayuela',
                'author': 'Julio Cortázar',
                'publication_year': 1963,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'El túnel',
                'author': 'Ernesto Sabato',
                'publication_year': 1948,
                'stock': random.randint(1, 10)
            },
            {
                'title': 'Ficciones',
                'author': 'Jorge Luis Borges',
                'publication_year': 1944,
                'stock': random.randint(1, 10)
            }
        ]
        
        for book_data in books_data:
            Book.objects.create(**book_data)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully with books and admin user'))
