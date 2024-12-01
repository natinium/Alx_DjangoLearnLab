from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework

class BookFilter(FilterSet):
    """
    Custom filter set for Book model
    Allows filtering by title, author name, and publication year
    """
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
            'publication_year': ['exact', 'gt', 'lt', 'gte', 'lte'],
        }

class ListView(generics.ListAPIView):
    """
    List view for books with advanced filtering, searching and ordering.
    
    Filter options:
    - title: exact match or contains (case-insensitive)
    - author__name: exact match or contains (case-insensitive)
    - publication_year: exact, greater than, less than, greater or equal, less or equal
    
    Search functionality:
    - Searches across title and author name fields
    
    Ordering options:
    - Can order by title, publication_year, author__name
    
    Example URLs:
    - Filter: /api/books/?title__icontains=python&publication_year__gte=2020
    - Search: /api/books/?search=django
    - Order: /api/books/?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable all filter backends
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    # Configure filtering
    filterset_class = BookFilter
    
    # Configure searching
    search_fields = ['title', 'author__name']
    
    # Configure ordering
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']  # Default ordering

class DetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 


class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        if Book.objects.filter(title=title).exists():
            raise ValidationError({"detail": "A book with this title already exists."})
        serializer.save()

class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 

    def perform_update(self, serializer):
        publication_year = serializer.validated_data.get('publication_year')
        if publication_year > 2024:
            raise ValidationError({"detail": "Publication year cannot be in the future."})
        serializer.save()


class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  
