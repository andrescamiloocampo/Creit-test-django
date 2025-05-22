from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Book, CustomUser, BorrowRecord

class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'
    paginate_by = 8

class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'publication_year', 'stock']
    template_name = 'library/book_form.html'
    
    def test_func(self):
        return self.request.user.is_admin()
    
    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'publication_year', 'stock']
    template_name = 'library/book_form.html'
    
    def test_func(self):
        return self.request.user.is_admin()
    
    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.pk})

def borrow_book(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to login to borrow books.")
        return redirect('login')
        
    if hasattr(request.user, 'is_admin') and request.user.is_admin():
        messages.warning(request, "Administrators cannot borrow books.")
        return redirect('book-list')
    
    book = get_object_or_404(Book, pk=pk)
    
    if book.stock < 1:
        messages.warning(request, "This book is currently out of stock.")
        return redirect('book-detail', pk=pk)
        
    existing_borrow = BorrowRecord.objects.filter(
        user=request.user, 
        book=book,
        returned=False
    ).exists()
    
    if existing_borrow:
        messages.warning(request, "You already have this book borrowed.")
        return redirect('book-detail', pk=pk)
    
    BorrowRecord.objects.create(user=request.user, book=book)
    book.stock -= 1
    book.save()
    
    messages.success(request, f"You have successfully borrowed {book.title}.")
    return redirect('book-detail', pk=pk)

def return_book(request, pk):
    if not request.user.is_authenticated or request.user.is_admin():
        messages.warning(request, "Only regular users can return books.")
        return redirect('book-list')
    
    book = get_object_or_404(Book, pk=pk)
    
    borrow_record = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        returned=False
    ).first()
    
    if not borrow_record:
        messages.warning(request, "You don't have this book borrowed.")
        return redirect('book-detail', pk=pk)
    
    borrow_record.returned = True
    borrow_record.return_date = timezone.now()
    borrow_record.save()
    
    book.stock += 1
    book.save()
    
    messages.success(request, f"You have successfully returned {book.title}.")
    return redirect('book-detail', pk=pk)

class UserBooksView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BorrowRecord
    template_name = 'library/user_books.html'
    context_object_name = 'borrow_records'
    
    def test_func(self):
        return not self.request.user.is_admin()
    
    def get_queryset(self):
        return BorrowRecord.objects.filter(user=self.request.user).order_by('-borrow_date')