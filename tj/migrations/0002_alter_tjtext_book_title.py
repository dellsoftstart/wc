# Generated by Django 4.2.1 on 2024-01-26 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tjtext',
            name='book_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название произведения'),
        ),
    ]
