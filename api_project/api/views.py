from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAuthorOrReadOnly

class BookList(generics.ListAPIView): 
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet): 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
