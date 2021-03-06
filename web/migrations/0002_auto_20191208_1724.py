# Generated by Django 2.2.7 on 2019-12-08 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(choices=[('C', 'C'), ('JAVA', 'JAVA'), ('PYTHON', 'PYTHON')], max_length=10, unique=True, verbose_name='skill')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='summary',
        ),
        migrations.AddField(
            model_name='card',
            name='summary',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='skills',
            field=models.ManyToManyField(to='web.Skill'),
        ),
    ]
