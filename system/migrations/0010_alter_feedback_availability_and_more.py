# Generated by Django 4.1.2 on 2022-10-24 08:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_feedback_approved_alter_hospital_pass_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='availability',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='collaboration_rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='communication_rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='treatment_rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='pass_key',
            field=models.CharField(default='49r3dicnap', max_length=100, unique=True),
        ),
    ]
