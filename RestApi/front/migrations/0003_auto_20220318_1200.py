# Generated by Django 3.2 on 2022-03-18 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_assign_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='assign',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='assign',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='semester',
            field=models.CharField(max_length=10, null=True),
        ),
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
        migrations.AlterField(
            model_name='item',
            name='year',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
