# Generated by Django 2.2.7 on 2019-12-18 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_course_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-createTime']},
        ),
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(default=''),
        ),
    ]