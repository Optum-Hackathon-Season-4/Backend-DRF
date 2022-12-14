# Generated by Django 4.1.2 on 2022-10-24 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_alter_feedback_availability_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicinesforPrescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('time_to_taken', models.CharField(choices=[('Morning Before Breakfast', 'Morning Before Breakfast'), ('Morning After Breakfast', 'Morning After Breakfast'), ('Afternoon Before Lunch', 'Afternoon Before Lunch'), ('Afternoon After Lunch', 'Afternoon After Lunch'), ('Night Before Dinner', 'Night Before Dinner'), ('Night After Dinner', 'Afternoon After Dinner')], max_length=100)),
                ('cost', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='hospital',
            name='pass_key',
            field=models.CharField(default='qwgu0h5d7x', max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField()),
                ('follow_up', models.BooleanField()),
                ('date', models.DateField(auto_now_add=True)),
                ('symptoms', models.TextField()),
                ('payment_deadline', models.DateField(blank=True, null=True)),
                ('paid', models.BooleanField(blank=True, default=False, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.doctor')),
                ('medicines', models.ManyToManyField(to='system.medicinesforprescription')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.patient')),
            ],
        ),
    ]
