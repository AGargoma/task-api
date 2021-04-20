# Generated by Django 3.2 on 2021-04-19 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Quiz', max_length=100)),
                ('deadline', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('state', models.CharField(choices=[('assigned', 'Assigned'), ('completed', 'Completed'), ('assessed', 'Assessed')], default='assigned', max_length=10)),
                ('correct_answer_count', models.IntegerField(default=0, editable=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
            ],
        ),
    ]