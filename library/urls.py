from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('book/new/', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    
    path('borrow/<int:pk>/', views.borrow_book, name='borrow-book'),
    path('return/<int:pk>/', views.return_book, name='return-book'),
    path('my-books/', views.UserBooksView.as_view(), name='user-books'),
    
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='library/logout.html'), name='logout'),
    
    path('api/', include('library.api.urls', namespace='api')),
]