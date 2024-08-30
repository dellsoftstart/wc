# Generated by Django 4.2.1 on 2024-02-01 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ru', '0002_g1level_g1_lexical_div_q_l1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='g4level',
            name='g4_lexical_div_q_l1',
            field=models.FloatField(blank=True, null=True, verbose_name='Лексическое разнообразие 4.1'),
        ),
        migrations.AddField(
            model_name='g4level',
            name='g4_lexical_div_q_l2',
            field=models.FloatField(blank=True, null=True, verbose_name='Лексическое разнообразие 4.2'),
        ),
    ]
