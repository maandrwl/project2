# Generated by Django 3.2 on 2022-04-10 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0010_auto_20220410_1116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assign',
            old_name='item',
            new_name='subject',
        ),
    ]
