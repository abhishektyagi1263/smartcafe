# Generated by Django 3.0.3 on 2021-08-21 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0003_ordermodel_items_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]