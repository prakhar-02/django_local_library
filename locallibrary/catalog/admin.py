from django.contrib import admin
from .models import Book, BookInstance, Language, Genre, Author

# Register your models here.

# admin.site.register(Book)
# admin.site.register(BookInstance)
# #admin.site.register(Author)
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    
class BookInline(admin.TabularInline):
    model = Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back', 'id']
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None,{
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]    
    inlines = [BookInline]

admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)