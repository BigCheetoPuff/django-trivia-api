# Generated by Django 3.0.11 on 2021-08-09 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia_game', '0009_auto_20210808_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=300),
        ),
    ]