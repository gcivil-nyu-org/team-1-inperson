# Generated by Django 2.2 on 2022-10-28 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("landing_map", "0003_auto_20221025_2348"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="favorite",
            name="typeID",
        ),
    ]