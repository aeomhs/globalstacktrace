# Generated by Django 2.2.7 on 2019-12-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='created_at',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]
