# Generated by Django 4.2 on 2023-05-28 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nadlan_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='content',
            new_name='message',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='title',
        ),
    ]
