# Generated by Django 5.1.5 on 2025-02-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_posts', '0010_remove_blogratingema_current_request_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
    ]
