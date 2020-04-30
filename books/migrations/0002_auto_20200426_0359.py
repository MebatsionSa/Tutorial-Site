# Generated by Django 2.2.9 on 2020-04-26 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='course_id',
            new_name='course_code_id',
        ),
        migrations.AlterField(
            model_name='book',
            name='book_file',
            field=models.FileField(default='null', upload_to='books/uploads/'),
        ),
    ]