# Generated by Django 3.0.11 on 2021-08-09 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia_game', '0010_auto_20210808_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='answer_type',
            field=models.CharField(choices=[('N', 'NAME'), ('PL', 'PLACE'), ('AC', 'ACTION'), ('R', 'REASON'), ('I', 'ITEM'), ('AN', 'ANIMAL'), ('PE', 'PERSON'), ('NU', 'NUMBER'), ('DO', 'DOCTRINE')], max_length=10),
        ),
        migrations.AlterField(
            model_name='questioncategory',
            name='answer_type',
            field=models.CharField(choices=[('N', 'NAME'), ('PL', 'PLACE'), ('AC', 'ACTION'), ('R', 'REASON'), ('I', 'ITEM'), ('AN', 'ANIMAL'), ('PE', 'PERSON'), ('NU', 'NUMBER'), ('DO', 'DOCTRINE')], max_length=10),
        ),
    ]