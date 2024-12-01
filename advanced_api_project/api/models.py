from django.db import models

class Author(models.Model):
    """
    Represents an author who can write multiple books.
    
    """
    name = models.CharField(max_length=255)

class Book(models.Model):
    """
    Represents a book written by an author.

    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
