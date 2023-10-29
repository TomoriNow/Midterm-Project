from django.contrib import admin
from main.models import Book, Catalog_Entry, Book_Entry, Custom_Entry, BookPost, Profile

# Register your models here.
admin.site.register(Book)
admin.site.register(Book_Entry)
admin.site.register(Catalog_Entry)
admin.site.register(Custom_Entry)
admin.site.register(BookPost)
admin.site.register(Profile)
