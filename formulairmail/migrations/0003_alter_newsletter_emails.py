# Generated by Django 4.0.3 on 2022-05-12 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulairmail', '0002_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='emails',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
