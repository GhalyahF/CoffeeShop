# Generated by Django 2.1.4 on 2019-01-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycoffee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffee',
            name='foam',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='water',
            field=models.DecimalField(decimal_places=1, max_digits=1),
        ),
    ]
