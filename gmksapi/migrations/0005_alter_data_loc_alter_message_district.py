# Generated by Django 4.0.10 on 2023-05-03 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmksapi', '0004_alter_data_loc_alter_message_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='loc',
            field=models.CharField(choices=[('Purlia', 'Purlia'), ('Bankura', 'Bankura'), ('Birbhum', 'Birbhum'), ('Paschim Medinipur', 'Paschim Medinipur'), ('General', 'General'), ('Jhargram', 'Jhargram')], max_length=30),
        ),
        migrations.AlterField(
            model_name='message',
            name='district',
            field=models.CharField(choices=[('Purlia', 'Purlia'), ('Bankura', 'Bankura'), ('Birbhum', 'Birbhum'), ('Paschim Medinipur', 'Paschim Medinipur'), ('General', 'General'), ('Jhargram', 'Jhargram')], max_length=30),
        ),
    ]
