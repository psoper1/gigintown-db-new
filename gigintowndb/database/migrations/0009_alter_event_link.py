# Generated by Django 4.2.7 on 2023-11-18 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_alter_event_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='Link',
            field=models.TextField(blank='True', max_length=2000, null=True),
        ),
    ]