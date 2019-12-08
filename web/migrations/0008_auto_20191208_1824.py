# Generated by Django 2.2.7 on 2019-12-08 09:24

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20191208_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='skills',
        ),
        migrations.AddField(
            model_name='card',
            name='skill',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('C', 'C'), ('JAVA', 'JAVA'), ('PYTHON', 'PYTHON')], max_length=10, null=True, verbose_name='skill'),
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
