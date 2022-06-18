# Generated by Django 4.0.4 on 2022-05-28 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_book_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentaires',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecteur', models.IntegerField()),
                ('commentaire', models.TextField()),
                ('note', models.IntegerField()),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
            ],
        ),
    ]
