# Generated by Django 4.0.10 on 2023-05-03 17:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Awareness',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('event', models.CharField(max_length=1000)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('loc', models.CharField(max_length=300)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('loc', models.CharField(choices=[('General', 'General'), ('Purlia', 'Purlia'), ('Paschim Medinipur', 'Paschim Medinipur'), ('Bankura', 'Bankura'), ('Jhargram', 'Jhargram'), ('Birbhum', 'Birbhum')], max_length=30)),
                ('language', models.CharField(choices=[('en', 'English'), ('bn', 'Bengali')], max_length=4)),
                ('category', models.CharField(max_length=30)),
                ('upload', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=1000)),
                ('district', models.CharField(choices=[('General', 'General'), ('Purlia', 'Purlia'), ('Paschim Medinipur', 'Paschim Medinipur'), ('Bankura', 'Bankura'), ('Jhargram', 'Jhargram'), ('Birbhum', 'Birbhum')], max_length=30)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True, unique=True)),
            ],
        ),
    ]
