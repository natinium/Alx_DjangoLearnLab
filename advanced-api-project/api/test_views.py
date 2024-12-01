from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Book, Author
from .serializers import BookSerializer

class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.author = Author.objects.create(name='Test Author')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Python Programming',
            publication_year=2022,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Django REST Framework',
            publication_year=2023,
            author=self.author
        )
        
        # Initialize API client
        self.client = APIClient()

    def test_list_books_unauthenticated(self):
        url = reverse('book-list')
        response = self.client.get(url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title='New Book').publication_year, 2024)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Title',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filtering_books(self):
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 2022})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Programming')

    def test_searching_books(self):
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Django'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django REST Framework')

    def test_ordering_books(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Django REST Framework')

    def test_invalid_publication_year(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2025,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_book_title(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'Python Programming',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)