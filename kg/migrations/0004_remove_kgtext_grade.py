# Generated by Django 4.2.1 on 2024-03-08 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kg', '0003_kgtext_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kgtext',
            name='grade',
        ),
    ]