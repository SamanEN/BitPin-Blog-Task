# Generated by Django 5.1.5 on 2025-02-03 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_posts', '0009_blogratingema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogratingema',
            name='current_request_rate',
        ),
    ]
