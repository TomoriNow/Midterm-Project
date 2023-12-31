# Generated by Django 4.2.6 on 2023-10-26 23:06

from django.db import migrations
from django.core.management import call_command


def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "books.json")

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_book_taggits_alter_book_name'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]