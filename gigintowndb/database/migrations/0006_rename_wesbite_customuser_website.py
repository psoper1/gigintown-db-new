# Generated by Django 4.2.7 on 2023-11-17 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_customuser_address_customuser_businessname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='wesbite',
            new_name='website',
        ),
    ]