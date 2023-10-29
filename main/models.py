from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager
import datetime

NOVEL = "Novel"
MANGA = "Manga"
MANHWA = "Manhwa"
LIGHT_NOVEL = "Light Novel"
TYPE_CHOICES = [
    (MANGA, "Manga"),
    (MANHWA, "Manhwa"),
    (LIGHT_NOVEL, "Light Novel"),
    (NOVEL, "Novel")
]
class Book(models.Model):
    name = models.CharField(max_length=255)
    imagelink = models.CharField(max_length=300, null=True, blank= True)
    type = models.CharField(max_length=15,choices=TYPE_CHOICES, default=MANGA)
    author = models.CharField(max_length = 30, null=True, blank= True)
    description = models.TextField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    taggits = TaggableManager(blank=True)
    
    def __str__(self):
        return self.name
    #TODO: Tags


class Book_Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    READING = "R"
    FINISHED = "F"
    DROPPED = "D"
    ON_HOLD = "O"
    PLAN_TO_READ = "P"
    STATUS_CHOICES = [
        (PLAN_TO_READ, "Plan to read"),
        (READING, "Reading"),
        (FINISHED, "Finished"),
        (ON_HOLD, "On Hold"),
        (DROPPED, "Dropped")
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PLAN_TO_READ)
    last_chapter_read = models.IntegerField(null=True, blank= True)
    last_read_date = models.DateField()
    review = models.TextField(null=True, blank= True)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)],null=True, blank= True)
    notes = models.TextField(null=True, blank=True)

class Catalog_Entry(models.Model):
    entry = models.OneToOneField(
        Book_Entry, on_delete=models.CASCADE, primary_key=True
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    def __str__(self):
        return '%s' % (self.book)

class Custom_Entry(models.Model):
    entry = models.OneToOneField(
        Book_Entry, on_delete=models.CASCADE, primary_key=True
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=15,choices=TYPE_CHOICES, default=MANGA)
    author = models.CharField(max_length = 30, null=True, blank= True)
    imagelink = models.CharField(max_length=300, null=True, blank= True)
    description = models.TextField(null=True, blank= True)
    taggits = TaggableManager(blank = True)

    def __str__(self):
        return '%s' % (self.name)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50)

class BookPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    imagelink = models.CharField(max_length=300, null=True, blank= True)
    type = models.CharField(max_length=15,choices=TYPE_CHOICES, default=MANGA)
    author = models.CharField(max_length = 30, null=True, blank= True)
    description = models.TextField(null=True, blank=True)
    taggits = TaggableManager(blank=True)