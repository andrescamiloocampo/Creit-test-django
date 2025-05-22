from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, BorrowViewSet, LoginView

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:pk>/borrow/', BorrowViewSet.as_view({'post': 'borrow'}), name='book-borrow'),
    path('books/<int:pk>/return/', BorrowViewSet.as_view({'post': 'return_book'}), name='book-return'),
    path('auth/login/', LoginView.as_view(), name='api-login'),
]