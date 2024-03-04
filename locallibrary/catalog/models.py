from django.db import models

from django.urls import reverse

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

import uuid
# Create your models here.

class Genre(models.Model):
    
    name = models.CharField(
        max_length=200,
        unique=True, 
        help_text="Enter a book genre (e.g. Science fiction, adventure etc.)"
    )

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Genre already exists (case insensitive match)"
            )
        ]

class Language(models.Model):

    name = models.CharField(max_length=100, unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    
    def get_absolute_url(self):
        return reverse("language-detail", args=[str(self.id)])

    def __str__(self) -> str:
        return self.name
    


class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    #By default on_delete=models.CASCADE, which means that if the author was deleted, 
    # this book would be deleted too! We use RESTRICT here, but we could also use PROTECT 
    # to prevent the author being deleted while any book uses it or SET_NULL to set the book's 
    # author to Null if the record is deleted.
    summary = models.TextField(max_length=1000, 
                               help_text="Enter a brief description of the book")
    
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>'
                            )
    
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    language = models.ForeignKey('Language', on_delete = models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'
    
class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta():
        ordering = ['due_back']

    def __str__(self) -> str:
        return f'{self.id}({self.book.title})'
    
class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse("author-details", args=[str(self.id)])
    
    def __str__(self):
        return f'{self.first_name}, {self.last_name}'
    