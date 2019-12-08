# Generated by Django 2.2.7 on 2019-12-08 12:50

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20191208_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='skill',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('C', 'C'), ('JAVA', 'JAVA'), ('PYTHON', 'PYTHON')], max_length=10, null=True, verbose_name='skill'),
        ),
    ]