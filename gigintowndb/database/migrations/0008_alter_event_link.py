# Generated by Django 4.2.7 on 2023-11-18 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_event_created_by_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='Link',
            field=models.TextField(default='www.nothing.com', max_length=2000, null=True),
        ),
    ]