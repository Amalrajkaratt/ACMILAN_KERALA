# Generated by Django 4.1.5 on 2023-04-15 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_rename_primary_mobile_number_coordinator_primary_mobile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordinator',
            name='center',
        ),
        migrations.AddField(
            model_name='coordinator',
            name='centers',
            field=models.ManyToManyField(to='Core.center'),
        ),
    ]
