# Generated by Django 4.0.1 on 2023-02-12 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0011_alter_annoucement_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annoucement',
            name='main_image',
            field=models.ImageField(blank=True, upload_to='announcement_images/'),
        ),
    ]
