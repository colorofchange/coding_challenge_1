# Generated by Django 3.2.7 on 2021-09-21 17:50

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templates_app', '0024_auto_20210914_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='from_line',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='reply_to',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='email_editions', to='templates_app.Tag'),
        ),
    ]
