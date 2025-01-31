# Generated by Django 5.1.5 on 2025-01-31 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_posts', '0003_alter_blogratingleakybucket_leak_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogratingleakybucket',
            name='blog_post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leaky_bucket', to='blog_posts.blogpost'),
        ),
    ]
