from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Book_Entry, Book, Custom_Entry, Catalog_Entry, Post, BookPost, Profile
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class BookSerializer(TaggitSerializer, serializers.ModelSerializer):
    taggits = TagListSerializerField()

    class Meta:
        model = Book
        fields = "__all__"

class CustomSerializer(TaggitSerializer, serializers.ModelSerializer):
    taggits = TagListSerializerField()
    class Meta:
        model = Custom_Entry
        fields = "__all__"

class Catalog_EntrySerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Catalog_Entry
        fields = ['book', ]

class Book_EntrySerializer(serializers.ModelSerializer):
    catalog_entry = Catalog_EntrySerializer(read_only=True)
    custom_entry = CustomSerializer(read_only=True)
        
    class Meta:
        model = Book_Entry
        fields = ['status', 'last_chapter_read', 'catalog_entry', 'last_read_date', 'custom_entry', 'review', 'rating', 'pk', 'notes']
        
class BookPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    taggits = TagListSerializerField()

    class Meta:
        model = BookPost
        fields = "__all__"
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"