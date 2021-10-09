# Generated by Django 3.1.7 on 2021-09-18 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionsoptions',
            old_name='option_1',
            new_name='option_text',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='user',
        ),
        migrations.RemoveField(
            model_name='questionsoptions',
            name='option_2',
        ),
        migrations.RemoveField(
            model_name='questionsoptions',
            name='option_3',
        ),
        migrations.RemoveField(
            model_name='questionsoptions',
            name='option_4',
        ),
        migrations.CreateModel(
            name='UserQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.questionsoptions')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]