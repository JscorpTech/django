# Generated by Django 5.0.2 on 2024-02-10 06:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('http', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]