from django.forms import ModelForm
from main.models import Custom_Entry, Book_Entry


class Book_EntryForm(ModelForm):
    class Meta:
        model = Book_Entry
        fields = ["status", "last_chapter_read", "review", "rating", "notes"]

class Custom_EntryForm(ModelForm):
    class Meta:
        model = Custom_Entry
        fields = ["name", "type", "author", "description", "imagelink"]