# Generated by Django 4.2.7 on 2023-11-19 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('express24', '0004_alter_shoppingcard_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcard',
            old_name='project',
            new_name='product',
        ),
    ]