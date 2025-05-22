from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from ..models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer,LoginSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsRegularUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'regular'

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

class BorrowViewSet(viewsets.ViewSet):
    permission_classes = [IsRegularUser]
    
    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        
        if book.stock < 1:
            return Response(
                {"detail": "Este libro no está disponible"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        record, created = BorrowRecord.objects.get_or_create(
            user=request.user,
            book=book,
            returned=False,
            defaults={'borrow_date': timezone.now()}
        )
        
        if not created:
            return Response(
                {"detail": "Ya tienes este libro prestado"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        book.stock -= 1
        book.save()
        
        return Response(
            {"detail": "Libro prestado exitosamente"},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        record = get_object_or_404(
            BorrowRecord,
            user=request.user,
            book=book,
            returned=False
        )
        
        record.returned = True
        record.return_date = timezone.now()
        record.save()
        
        book.stock += 1
        book.save()
        
        return Response(
            {"detail": "Libro devuelto exitosamente"},
            status=status.HTTP_200_OK
        )
        
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role
        },status=status.HTTP_200_OK)