# Generated by Django 3.1.4 on 2021-01-12 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='dateCompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
