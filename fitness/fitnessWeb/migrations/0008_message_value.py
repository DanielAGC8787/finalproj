# Generated by Django 4.0.4 on 2022-08-18 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessWeb', '0007_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='value',
            field=models.TextField(blank=True),
        ),
    ]
