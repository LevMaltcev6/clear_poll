# Generated by Django 3.1.4 on 2020-12-20 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='choice',
            field=models.ManyToManyField(blank=True, to='polls.ChoiceAnswer'),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('question', 'anon_token')},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='singlechoice',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='user',
        ),
    ]