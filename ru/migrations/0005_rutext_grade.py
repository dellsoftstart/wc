# Generated by Django 4.2.1 on 2024-02-08 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0004_g1level_g1_fre_oborneva_q_l1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutext',
            name='grade',
            field=models.IntegerField(blank=True, null=True, verbose_name='Класс'),
        ),
    ]
