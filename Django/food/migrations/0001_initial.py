# Generated by Django 4.2.7 on 2023-12-17 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('ms_unit', models.CharField(max_length=50)),
                ('purine_per_unit', models.FloatField()),
                ('health_tip', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='food')),
            ],
        ),
    ]
