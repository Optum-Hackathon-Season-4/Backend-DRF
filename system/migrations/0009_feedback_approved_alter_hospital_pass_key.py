# Generated by Django 4.1.2 on 2022-10-24 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_alter_hospital_pass_key_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='pass_key',
            field=models.CharField(default='q6ir9bmpnh', max_length=100, unique=True),
        ),
    ]
