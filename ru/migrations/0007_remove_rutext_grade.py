# Generated by Django 4.2.1 on 2024-03-08 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0006_alter_g3level_g3_lexical_div_q_l2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rutext',
            name='grade',
        ),
    ]
