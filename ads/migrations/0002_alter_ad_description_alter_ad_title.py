# Generated by Django 4.2.21 on 2025-05-21 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ads", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ad",
            name="description",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="ad",
            name="title",
            field=models.CharField(max_length=250),
        ),
    ]
