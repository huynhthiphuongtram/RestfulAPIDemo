# Generated by Django 4.1.7 on 2023-02-17 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(null=True, upload_to='courses/%Y/%m'),
        ),
    ]
