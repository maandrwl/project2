# Generated by Django 3.2 on 2022-04-06 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_auto_20220401_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='CourseName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='code',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('CourseName', 'code', 'semester', 'year')},
        ),
    ]
