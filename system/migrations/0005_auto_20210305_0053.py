# Generated by Django 3.1.4 on 2021-03-04 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20210305_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='user',
        ),
        migrations.AddField(
            model_name='students',
            name='admin',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='system.customuser'),
            preserve_default=False,
        ),
    ]
