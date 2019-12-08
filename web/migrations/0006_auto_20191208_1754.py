# Generated by Django 2.2.7 on 2019-12-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_merge_20191208_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='skill',
            field=models.CharField(choices=[('C', 'C'), ('JAVA', 'JAVA'), ('PYTHON', 'PYTHON')], max_length=10, verbose_name='skill'),
        ),
    ]