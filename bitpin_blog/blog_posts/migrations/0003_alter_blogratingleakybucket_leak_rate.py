# Generated by Django 5.1.5 on 2025-01-31 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_posts', '0002_blogratingleakybucket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogratingleakybucket',
            name='leak_rate',
            field=models.IntegerField(default=0),
        ),
    ]
