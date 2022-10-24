# Generated by Django 4.1.2 on 2022-10-24 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_alter_hospital_pass_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cost', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('Medical Test', 'Medical Test'), ('Operation', 'Operation'), ('Drug', 'Drug')], max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='hospital',
            name='pass_key',
            field=models.CharField(default='3bx68czqya', max_length=100, unique=True),
        ),
    ]