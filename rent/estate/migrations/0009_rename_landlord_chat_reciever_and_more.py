# Generated by Django 4.0.1 on 2023-01-28 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0008_alter_message_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='landlord',
            new_name='reciever',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='renter',
            new_name='sender',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='sender',
            new_name='writer',
        ),
    ]
