# Generated by Django 4.0.4 on 2022-08-27 01:50

from django.db import migrations, models
import fitnessWeb.models


class Migration(migrations.Migration):

    dependencies = [
        ('fitnessWeb', '0009_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.ImageField(blank=True, default='images/user.png', null=True, upload_to=fitnessWeb.models.get_image_path),
        ),
    ]
