# Generated by Django 3.0.3 on 2021-08-21 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0005_auto_20210821_1216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='id',
            new_name='no',
        ),
    ]
