# Generated by Django 4.2.6 on 2023-10-28 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_custom_entry_taggits'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_entry',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
