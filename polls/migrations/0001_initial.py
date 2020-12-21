# Generated by Django 3.1.4 on 2020-12-14 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField(editable=False)),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('type', models.CharField(choices=[('text', 'Text answer'), ('singlechoice', 'single option'), ('multichoice', 'many options')], default='text', max_length=50)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='polls.poll')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='polls.question')),
            ],
            options={
                'unique_together': {('text', 'question')},
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('user', models.IntegerField(blank=True, null=True)),
                ('anon_token', models.CharField(blank=True, max_length=256, null=True)),
                ('singlechoice', models.ManyToManyField(blank=True, to='polls.ChoiceAnswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
            ],
            options={
                'unique_together': {('question', 'user', 'anon_token')},
            },
        ),
    ]
