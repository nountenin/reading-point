# Generated by Django 4.0.3 on 2022-04-13 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0002_alter_events_descriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='image_events',
            field=models.ImageField(blank=True, null=True, upload_to='events/images/'),
        ),
    ]
