# Generated by Django 4.2.1 on 2024-03-08 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tj', '0005_tjtext_grade_alter_g1level_g1_lexical_div_q_l1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tjtext',
            name='grade',
        ),
    ]