# Generated by Django 3.2 on 2022-04-06 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0005_auto_20220406_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='assigns',
            field=models.ManyToManyField(to='front.Assign'),
        ),
    ]