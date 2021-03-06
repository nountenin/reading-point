# Generated by Django 4.0.3 on 2022-04-12 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pointlectureEmetteur', models.IntegerField()),
                ('pointlectureDestinateur', models.IntegerField()),
                ('dateTransfert', models.DateTimeField(auto_now_add=True)),
                ('desciption', models.TextField(null=True)),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Item_transfert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField()),
                ('created_by', models.IntegerField(default=1)),
                ('modified_by', models.IntegerField(default=1)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1)),
                ('livre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('transfert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.transfert')),
            ],
        ),
    ]
