# Generated by Django 2.1.1 on 2018-09-24 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20180924_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='position_title',
            new_name='title',
        ),
    ]
