# Generated by Django 5.0.4 on 2024-04-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='tasks_completed',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Tasks Completed'),
        ),
    ]
