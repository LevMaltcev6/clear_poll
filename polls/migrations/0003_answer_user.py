# Generated by Django 3.1.4 on 2020-12-20 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20201220_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]