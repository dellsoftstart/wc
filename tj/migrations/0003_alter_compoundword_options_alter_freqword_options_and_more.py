# Generated by Django 4.2.1 on 2024-01-26 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj', '0002_alter_tjtext_book_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compoundword',
            options={'verbose_name': 'Составные слова', 'verbose_name_plural': 'Составные слова'},
        ),
        migrations.AlterModelOptions(
            name='freqword',
            options={'verbose_name': 'Часто используемые слова', 'verbose_name_plural': 'Часто используемые слова'},
        ),
        migrations.AlterModelOptions(
            name='lcword',
            options={'verbose_name': 'Сложные слова', 'verbose_name_plural': 'Сложные слова'},
        ),
        migrations.AlterModelOptions(
            name='rareword',
            options={'verbose_name': 'Редкие слова', 'verbose_name_plural': 'Редкие слова'},
        ),
        migrations.AlterModelOptions(
            name='tjtext',
            options={'verbose_name': 'Текст на таджикском', 'verbose_name_plural': 'Тексты на таджикском'},
        ),
        migrations.AlterField(
            model_name='compoundword',
            name='compound_words',
            field=models.TextField(blank=True, null=True, verbose_name='Составные слова'),
        ),
        migrations.AlterField(
            model_name='freqword',
            name='freq_words',
            field=models.TextField(blank=True, null=True, verbose_name='Часто используемые слова'),
        ),
        migrations.AlterField(
            model_name='lcword',
            name='lc_words',
            field=models.TextField(blank=True, null=True, verbose_name='Сложные слова'),
        ),
        migrations.AlterField(
            model_name='rareword',
            name='rare_words',
            field=models.TextField(blank=True, null=True, verbose_name='Редкие слова'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='all_compound_words_p',
            field=models.FloatField(blank=True, null=True, verbose_name='% сложных слов '),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='book_author',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='complex_w_q',
            field=models.FloatField(blank=True, null=True, verbose_name='Кол-во составных слов'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='compound_w_q',
            field=models.FloatField(blank=True, null=True, verbose_name='Сложные слова и слова с дефисом'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='fw_p',
            field=models.FloatField(blank=True, null=True, verbose_name='% Часто используемых слов'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='fw_q',
            field=models.FloatField(blank=True, null=True, verbose_name='Часто используемые слова'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='level_result',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Рекомендуемый класс'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='multisyllabic_wq',
            field=models.FloatField(blank=True, null=True, verbose_name='Кол-во многосложных слов'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='rareword_p',
            field=models.FloatField(blank=True, null=True, verbose_name='% редких слов'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='rareword_q',
            field=models.FloatField(blank=True, null=True, verbose_name='Кол-во редких слов для 1-4 классов'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='sentence_avg',
            field=models.FloatField(blank=True, null=True, verbose_name='Ср. длина слова в слогах'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='sentence_q',
            field=models.IntegerField(blank=True, null=True, verbose_name='Общее кол-во предложений'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='uniq_w',
            field=models.IntegerField(blank=True, null=True, verbose_name='Кол-во уникальных слов'),
        ),
        migrations.AlterField(
            model_name='tjtext',
            name='words_q',
            field=models.IntegerField(blank=True, null=True, verbose_name='Общее кол-во слов'),
        ),
    ]
