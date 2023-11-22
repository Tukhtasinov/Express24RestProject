# Generated by Django 4.2.7 on 2023-11-19 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express24', '0005_rename_project_shoppingcard_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcard',
            name='is_ordered',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='shoppingcard',
            name='count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
