# Generated by Django 5.0.1 on 2024-01-08 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadcast', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(unique=True),
        ),
    ]
