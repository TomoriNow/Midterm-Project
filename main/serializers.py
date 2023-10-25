from rest_framework import serializers
from main.models import Book_Entry, Book, Custom_Entry, Catalog_Entry

class Book_EntrySerializer(serializers.ModelSerializer):
    catalog_entry = serializers.StringRelatedField()
    custom_entry = serializers.StringRelatedField()
        
    class Meta:
        model = Book_Entry
        fields = ['status', 'last_chapter_read', 'catalog_entry', 'custom_entry']

