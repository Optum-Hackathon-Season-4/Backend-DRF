# Generated by Django 4.1.2 on 2022-10-24 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_alter_hospital_pass_key_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='pass_key',
            field=models.CharField(default='asoq2b9nmf', max_length=100, unique=True),
        ),
    ]
