# Generated by Django 2.2.7 on 2019-12-15 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
