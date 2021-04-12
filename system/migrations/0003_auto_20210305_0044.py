# Generated by Django 3.1.4 on 2021-03-04 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20210305_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='admin',
        ),
        migrations.AddField(
            model_name='students',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='system.customuser'),
            preserve_default=False,
        ),
    ]
