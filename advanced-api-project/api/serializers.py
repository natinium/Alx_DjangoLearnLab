from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Serializes all fields of the Book model and includes
    custom validation for the `publication_year` field.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']  # Serializes all fields of the Book model

    def validate_publication_year(self, value):
        """
        Custom validation to ensure the publication year is not in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes the `name` field and dynamically serializes related Book objects
    using a nested BookSerializer.
    """
    books = BookSerializer(many=True, read_only=True)  # Related books serialized as nested objects

    class Meta:
        model = Author
        fields = ['name', 'books']  # Serializes only the `name` field and nested `books`
