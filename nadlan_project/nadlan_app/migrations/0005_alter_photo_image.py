# Generated by Django 4.2 on 2023-06-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nadlan_app', '0004_alter_tip_real_estate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.CharField(max_length=20),
        ),
    ]